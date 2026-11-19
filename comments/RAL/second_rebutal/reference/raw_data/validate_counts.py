#!/usr/bin/env python3
"""Check evaluation counts, aggregation, statistics, and the paper's LaTeX tables."""
import argparse
import json
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

METRICS = ('lift_success', 'unsafe_event', 'harmful_collision', 'object_escape',
           'palm_flipped', 'hand_too_far')
LABELS = ('Lift Success', 'Unsafe Rate Avg', 'Harmful collision', 'Object escape',
          'Palm flipped', 'Hand too far')
checks = 0
errors = []


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def rounded(value, digits=1):
    return float(Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP))


def percent(count, trials):
    return float((Decimal(count) * 100 / Decimal(trials)).quantize(Decimal('.1'), rounding=ROUND_HALF_UP))


def load(path):
    return json.loads(path.read_text())


def text(path):
    # Strip formatting commands but retain values and TeX row terminators.
    return re.sub(r'\\[a-zA-Z]+', '', path.read_text()).replace('{', '').replace('}', '')


def rows(path, label):
    return [list(map(float, re.findall(r'\d+\.\d+', row))) for row in
            re.findall(r'^\s*' + label + r'\s*&(.+?)(?=\\\\)', text(path), re.I | re.M | re.S)]


def same(actual, expected, message):
    check(actual == expected, f'{message}: got {actual}, expected {expected}')


def metric_counts(row, location):
    if 'metrics' in row:
        for name, metric in row['metrics'].items():
            if 'count' in metric:
                c, n = metric['count'], row['trials']
                check(isinstance(c, int) and 0 <= c <= n, f'{location}/{name}: invalid count')
                same(percent(c, n), metric['reported_percent'], f'{location}/{name} rate')
            else:
                check(not any(k.startswith(('compatible', 'nearest')) for k in metric),
                      f'{location}/{name}: candidate count metadata remains')


def wilson(c, n):
    z = 1.959963984540054
    p = c / n
    center = (p + z*z/(2*n)) / (1+z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1+z*z/n)
    return [rounded(100*(center-half)), rounded(100*(center+half))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paper_root', type=Path, help='Path to RAL_dexsafedagger checkout')
    args = parser.parse_args()
    root = args.paper_root.resolve()
    data = Path(__file__).resolve().parent
    hardware = load(data/'real_robot_counts.json')
    simulation = load(data/'simulation_results.json')
    teacher = load(data/'teacher_table_ii_mean_aggregate.json')

    for row in hardware['per_object']:
        counts = row['counts']
        for name, c in counts.items():
            check(isinstance(c, int) and 0 <= c <= row['trials'], f'{row["object"]}/{name}: invalid count')
            same(percent(c, row['trials']), row['reported_percent'][name], f'{row["object"]}/{name}')
        same(sum(counts[k] for k in METRICS[2:]), counts['unsafe_event'], f'{row["object"]} unsafe decomposition')

    for group in hardware['group_totals_from_per_object_rows']:
        members = [r for r in hardware['per_object'] if r['group'] == group['group']]
        same(len(members), group['objects'], f'{group["group"]} object count')
        same(sum(r['trials'] for r in members), group['trials'], f'{group["group"]} trials')
        for name in METRICS:
            total = sum(r['counts'][name] for r in members)
            same(total, group['counts'][name], f'{group["group"]}/{name} sum')
            same(percent(total, group['trials']), group['percent_rounded_1dp'][name], f'{group["group"]}/{name} pooled rate')

    for row in hardware['reported_aggregates']:
        metric_counts(row, f'{row["source_table"]}/{row["policy"]}/{row["group"]}')
        # An exact pooled percentage must have an integer numerator at this denominator.
        for name, metric in row['metrics'].items():
            if 'count' not in metric:
                check(any(percent(c, row['trials']) == metric['reported_percent'] for c in range(row['trials']+1)),
                      f'{row["policy"]}/{row["group"]}/{name}: {metric["reported_percent"]}% is impossible at {row["trials"]} trials; author count required')

    metric_counts({'trials': teacher['total_trials'], 'metrics': teacher['metrics']}, 'teacher all 40')
    same(sum(teacher['metrics'][k]['count'] for k in METRICS[2:]), teacher['metrics']['unsafe_event']['count'], 'teacher unsafe decomposition')
    for row in simulation['table_II_teacher_policy']:
        metric_counts(row, f'teacher/{row["scope"]}')
    for row in simulation['table_III_student_ablations']:
        for evaluation in row['evaluations']:
            metric_counts(evaluation, f'ablation {row["ablation"]}/{evaluation["scope"]}')
    metric_counts(simulation['appendix_table_3_critic'], 'critic')

    table = root/'table'
    for k, label in zip(METRICS, LABELS):
        actual = rows(table/'teacher_performance.tex', label)[0]
        same(actual, [r['metrics'][k]['reported_percent'] for r in simulation['table_II_teacher_policy']], f'Table II/{k}')
        actual = rows(table/'real_world_results.tex', label)[0]
        objects = hardware['per_object'][:6]
        expected = [r['reported_percent'][k] for r in objects] + [g['percent_rounded_1dp'][k] for g in hardware['group_totals_from_per_object_rows']]
        same(actual, expected, f'Table IV(a)/{k}')
        actual = rows(table/'appendix_additional_experimental_results.tex', label)
        expected = [r['reported_percent'][k] for r in hardware['per_object'][6:]]
        same(sum(actual, []), expected, f'Appendix Table 5/{k}')

    for ablation in simulation['table_III_student_ablations']:
        actual = rows(table/'ablation_studies.tex', r'\('+ablation['ablation']+r'\)')[0]
        expected = [r['metrics'][k]['reported_percent'] for r in ablation['evaluations'] for k in METRICS[:2]]
        same(actual, expected, f'Table III/{ablation["ablation"]}')

    for filename in ('real_world_results.tex', 'appendix_physical_baseline_comparison.tex'):
        for label, k in [('Lift success', 'lift_success'), ('Unsafe-event rate', 'unsafe_event')]:
            expected = [r['metrics'][k]['reported_percent'] for r in hardware['reported_aggregates'][4:]]
            same(rows(table/filename, label)[-1], expected, f'{filename}/{k}')

    critic = simulation['appendix_table_3_critic']
    expected = [critic['metrics'][k]['reported_percent'] for k in ('lift_success', 'unsafe_event', 'task_outcome_prediction_accuracy')]
    conditional = critic['conditional_unsafe_episode_metrics']
    expected += [conditional['reported_detection_percent'], conditional['reported_false_negative_percent']]
    for label, value in zip(('Lift-success rate', 'Unsafe-episode rate', 'Task-outcome prediction accuracy', 'Unsafe-episode detection rate', 'Unsafe false-negative rate'), expected):
        same(rows(table/'appendix_bellman_critic_evaluation.tex', label)[0], [value], f'Appendix Table 3/{label}')
    for label, k in [('Lift Success', 'lift_success'), ('Unsafe Rate', 'unsafe_event')]:
        line = next(line for line in (table/'appendix_ablation_across_seeds.tex').read_text().splitlines() if line.startswith(label))
        block = (table/'appendix_ablation_across_seeds.tex').read_text().split(line, 1)[1].split('\\\\', 1)[0]
        actual = list(map(float, re.findall(r'\d+\.\d+', block)))
        expected = [s['reported_seed_summary'][k][v] for s in simulation['appendix_table_4_across_seeds']['reported_summaries'] for v in ('mean_percent', 'sd_percentage_points')]
        same(actual, expected, f'Appendix Table 4/{k}')

    summary_labels = ('Lift success', 'Unsafe rate avg.', 'Harmful collision', 'Object escape', 'Palm flipped', 'Hand too far')
    for k, label in zip(METRICS, summary_labels):
        expected = []
        for group in hardware['group_totals_from_per_object_rows']:
            expected += [group['percent_rounded_1dp'][k]] + wilson(group['counts'][k], group['trials'])
        same(rows(table/'appendix_seen_unseen_summary.tex', re.escape(label))[0], expected, f'Appendix Table 6/{k} and Wilson intervals')

    appendix = root/'comments/RAL/second_rebutal/response/06_appendix.tex'
    for row in hardware['table_8_pooled_comparison']['rows']:
        n, c, d = row['trials_per_ablation'], row['c_unsafe_episodes'], row['d_unsafe_episodes']
        p1, p2 = c/n, d/n
        diff = p1-p2
        half = 1.959963984540054 * math.sqrt(p1*(1-p1)/n+p2*(1-p2)/n)
        interval = [rounded(100*(diff-half), 2), rounded(100*(diff+half), 2)]
        pooled = (c+d)/(2*n)
        z = diff/math.sqrt(pooled*(1-pooled)*2/n)
        p = math.erfc(abs(z)/math.sqrt(2))
        same(rounded(100*diff, 2), row['reduction_percentage_points'], f'{row["group"]} reduction')
        same(interval, row['normal_approximation_95_percent_ci_pp'], f'{row["group"]} difference interval')
        check(abs(p-row['two_sided_p_value']) < 1e-12, f'{row["group"]} p value')
        line = next(line for line in appendix.read_text().splitlines() if line.startswith(row['group'].capitalize()+' &'))
        actual = list(map(float, re.findall(r'-?\d+\.\d+', line)))
        same(actual, [percent(c,n), percent(d,n), rounded(100*diff,2)]+interval+[rounded(p,3)], f'Appendix Table 8/{row["group"]}')

    print(f'{checks} checks; {len(errors)} failures')
    for error in errors:
        print('FAIL:', error)
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
