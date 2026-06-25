"""
Лабораторна робота No 3
МОДЕЛЮВАННЯ ОДНОКАНАЛЬНОЇ СМО

Студент: Сергієнко Олексій Пі-243
Номер залікової книжки: 15128294
Варіант: 11 (A=7-9, B=4±1, C=14 годин)
"""

import sys
import os
import math

# Встановлюємо UTF-8 кодування для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ============================================================================
# Генерація рівномірних чисел з Lab 1 (мішаний метод)
# ============================================================================

def generate_uniform_lab1(n=100):
    """Генерація рівномірних псевдовипадкових чисел [0,1] мішаним методом"""
    a = 279
    m = 10000
    c = 3928
    x0_int = 8294

    x = x0_int
    numbers = []
    for _ in range(n):
        x = (a * x + c) % m
        numbers.append(x / m)
    return numbers

# ============================================================================
# Допоміжні функції
# ============================================================================

def uniform_random(a, b, rng):
    """Генерація рівномірно розподіленого випадкового числа на [a, b]"""
    return (b - a) * rng.pop(0) + a

def generate_exponential(lam, rng):
    """Генерація експоненціально розподіленого випадкового числа"""
    u = rng.pop(0)
    return -math.log(1 - u) / lam

# ============================================================================
# Моделювання одноканальної СМО
# ============================================================================

def simulate_single_channel_smo():
    """
    Моделювання одноканальної системи обслуговування.
    
    Параметри (варіант 11):
    - А = 7-9 хв (інтервал між заявками)
    - Б = 4±1 хв (час обслуговування)
    - В = 14 годин (тривалість моделювання = 840 хв)
    """
    print("\n" + "#"*70)
    print("#  ЛАБОРАТОРНА РОБОТА No 3")
    print("#  МОДЕЛЮВАННЯ ОДНОКАНАЛЬНОЇ СМО")
    print("#  Варіант 11: A=7-9, B=4±1, C=14 год")
    print("#"*70)

    # Параметри
    arrival_min = 7   # A мінімальний інтервал
    arrival_max = 9   # A максимальний інтервал
    service_mean = 4  # Б середній час
    service_delta = 1 # Б допуск
    service_min = service_mean - service_delta  # 3
    service_max = service_mean + service_delta  # 5
    simulation_hours = 14
    simulation_minutes = simulation_hours * 60  # 840 хв

    print(f"\n  Параметри системи:")
    print(f"    Інтервал приходу: [{arrival_min}; {arrival_max}] хв")
    print(f"    Час обслуговування: [{service_min}; {service_max}] хв")
    print(f"    Тривалість моделювання: {simulation_hours} год = {simulation_minutes} хв")

    # Розрахунок завантаження
    arrival_mean = (arrival_min + arrival_max) / 2  # 8 хв
    service_mean_actual = (service_min + service_max) / 2  # 4 хв
    utilization = service_mean_actual / arrival_mean

    print(f"\n  Розрахункові параметри:")
    print(f"    Середній інтервал приходу: {arrival_mean:.1f} хв")
    print(f"    Середній час обслуговування: {service_mean_actual:.1f} хв")
    print(f"    Коефіцієнт завантаження (ρ): {utilization:.4f}")

    if utilization >= 1.0:
        print(f"  УВАГА: Система нестабільна (ρ >= 1)! Черга буде нескінченно рости.")
    else:
        print(f"  Система стабільна (ρ < 1). Черга буде скінченною.")

    # Генерація випадкових чисел
    rng = generate_uniform_lab1(2000)

    # Стан системи
    current_time = 0.0
    next_arrival_time = 0.0
    service_end_time = float('inf')
    is_server_busy = False
    
    # Лічильники
    total_arrivals = 0
    total_served = 0
    total_wait_time = 0.0
    max_queue_length = 0
    
    # Часова статистика для графіків
    time_queue_length = []  # (час, довжина черги)
    
    queue_length = 0
    customer_wait = 0
    
    # Генерація першої заявки
    if rng:
        next_arrival_time = uniform_random(arrival_min, arrival_max, rng)
    
    print(f"\n{'='*70}")
    print(f"  ХІД МОДЕЛЮВАННЯ (вибірка)")
    print(f"{'='*70}")
    print(f"  {'Час':>8} | {'Подія':<20} | {'Черга':>5} | {'Сервер':>8}")
    print(f"  {'-'*8}-+-{'-'*20}-+-{'-'*5}-+-{'-'*8}")
    
    sample_count = 0
    max_sample = 30

    # Головний цикл моделювання
    max_events = 2000  # обмеження для безпеки
    event_count = 0

    while current_time < simulation_minutes and event_count < max_events:
        event_count += 1
        
        # Визначаємо наступну подію
        if next_arrival_time <= service_end_time:
            # Прихід заявки
            current_time = next_arrival_time
            
            if is_server_busy:
                queue_length += 1
                customer_wait = 0
                event_type = "Прихід (в чергу)"
            else:
                event_type = "Прихід (одразу)"
            
            total_arrivals += 1
            max_queue_length = max(max_queue_length, queue_length)
            
            # Запис статистики
            time_queue_length.append((current_time, queue_length))
            
            # Початок обслуговування
            service_time = uniform_random(service_min, service_max, rng)
            service_end_time = current_time + service_time
            is_server_busy = True
            
            # Генерація наступної заявки
            if rng:
                next_arrival_time = current_time + uniform_random(arrival_min, arrival_max, rng)
            
            if sample_count < max_sample:
                print(f"  {current_time:>7.1f} | {event_type:<20} | {queue_length:>5} | ЗАЙНЯТИЙ")
                sample_count += 1
        
        else:
            # Кінець обслуговування
            current_time = service_end_time
            total_served += 1
            queue_length -= 1
            
            if queue_length < 0:
                queue_length = 0
                is_server_busy = False
                service_end_time = float('inf')
                event_type = "Звільнення (порожньо)"
            else:
                event_type = "Звільнення (наступна)"
                service_time = uniform_random(service_min, service_max, rng)
                service_end_time = current_time + service_time
            
            # Запис статистики
            time_queue_length.append((current_time, queue_length))
            
            if sample_count < max_sample:
                print(f"  {current_time:>7.1f} | {event_type:<20} | {queue_length:>5} | ЗАЙНЯТИЙ")
                sample_count += 1

    # Обчислення статистики
    avg_queue_length = sum(q[1] for q in time_queue_length) / len(time_queue_length) if time_queue_length else 0

    print(f"\n  ... (показано {min(sample_count, max_sample)} з {event_count} подій) ...")

    print(f"\n{'='*70}")
    print(f"  РЕЗУЛЬТАТИ МОДЕЛЮВАННЯ")
    print(f"{'='*70}")
    print(f"\n  Загальна статистика:")
    print(f"    Загальна кількість заявок:        {total_arrivals}")
    print(f"    Кількість обслугованих:            {total_served}")
    print(f"    Максимальна довжина черги:         {max_queue_length}")
    print(f"    Середня довжина черги:             {avg_queue_length:.2f}")
    print(f"    Коефіцієнт завантаження (ρ):       {utilization:.4f}")
    print(f"    Тривалість моделювання:            {simulation_minutes} хв")

    print(f"\n  Аналіз завантаження:")
    if utilization < 0.7:
        print(f"    Система недостатньо завантажена (< 0.7)")
    elif utilization < 0.9:
        print(f"    Система оптимально завантажена (0.7 - 0.9)")
    else:
        print(f"    Система сильно завантажена (> 0.9)")

    # Графік довжини черги
    print(f"\n{'='*70}")
    print(f"  ГРАФІК ЗМІНИ ДОВЖИНИ ЧЕРГИ У ЧАСІ")
    print(f"{'='*70}")
    
    # Побудова графіку
    graph_width = 60
    graph_height = 10
    
    if time_queue_length:
        max_time = time_queue_length[-1][0]
        max_q = max(q[1] for q in time_queue_length) if time_queue_length else 1
        if max_q == 0:
            max_q = 1
        
        # Створення матриці графіку
        grid = [[' ' for _ in range(graph_width)] for _ in range(graph_height)]
        
        for i, (t, q) in enumerate(time_queue_length):
            x = int(t / max_time * (graph_width - 1))
            y = int(q / max_q * (graph_height - 1))
            if y < graph_height and x < graph_width:
                grid[graph_height - 1 - y][x] = '*'
        
        # Друк графіку
        print(f"\n  Довжина черги:")
        for i in range(0, graph_height, 2):
            label = f"  {max_q - i * (max_q // (graph_height//2)):<3} |"
            print(label + ''.join(grid[i]))
        
        # Вісь X
        axis = f"  {'0':>3} |" + '-' * (graph_width - 1)
        print(axis)
        print(f"       {'0':<10} {max_time/2:.0f}           {max_time:.0f} хв")
        print(f"       {'Час (хв)':^55}")

    # Коефіцієнт використання пристрою по інтервалах
    print(f"\n{'='*70}")
    print(f"  КОЕФІЦІЄНТ ВИКОРИСТАННЯ ПРИСТРОЮ")
    print(f"{'='*70}")
    
    # Розрахунок коефіцієнта використання по годинниках
    intervals = 84  # по 10 хвилин
    interval_length = simulation_minutes / intervals  # 10 хв
    
    print(f"\n  {'Інтервал':<15} | {'Використання':>10} | {'Статус':<15}")
    print(f"  {'-'*15}-+-{'-'*10}-+-{'-'*15}")
    
    for i in range(intervals):
        start_t = i * interval_length
        end_t = (i + 1) * interval_length
        
        # Знаходимо події в цьому інтервалі
        busy_time = 0
        for j in range(len(time_queue_length) - 1):
            t1 = time_queue_length[j][0]
            t2 = time_queue_length[j+1][0]
            
            if t1 >= start_t and t2 <= end_t:
                # Цей інтервал повністю в межах
                if time_queue_length[j][1] > 0:  # сервер зайнятий
                    busy_time += (t2 - t1)
        
        usage = busy_time / interval_length if interval_length > 0 else 0
        status = "ЗАЙНЯТИЙ" if usage > 0.5 else "ВІЛЬНИЙ"
        bar = '#' * int(usage * 10) + '-' * (10 - int(usage * 10))
        
        print(f"  {start_t:.0f}-{end_t:.0f} хм{'':<5} | {usage:>6.1%}  {bar:<10} | {status:<15}")

    print(f"\n{'='*70}")
    print(f"  ВИСНОВОК")
    print(f"{'='*70}")
    print(f"""
  1. Змоделювано роботу одноканальної СМО протягом {simulation_hours} год.
  2. Середній інтервал приходу заявок: {arrival_mean:.1f} хв
  3. Середній час обслуговування: {service_mean_actual:.1f} хв
  4. Коефіцієнт завантаження ρ = {utilization:.4f}
  5. Максимальна довжина черги: {max_queue_length}
  6. Середня довжина черги: {avg_queue_length:.2f}
  7. Система {'стабільна' if utilization < 1.0 else 'нестабільна'}
  
  Моделювання показало, що одноканальна СМО з даними параметрами
  {'має прийнятне навантаження' if utilization < 0.9 else 'потребує додаткового каналу обслуговування'}.
    """)

# ============================================================================
# Головна програма
# ============================================================================

def main():
    print("="*70)
    print("  ЛАБОРАТОРНА РОБОТА No 3")
    print("  МОДЕЛЮВАННЯ ОДНОКАНАЛЬНОЇ СМО")
    print("  Номер залікової книжки: 15128294")
    print("  Варіант: 11")
    print("="*70)
    
    simulate_single_channel_smo()
    
    print("\n" + "="*70)
    print("  КІНЕЦЬ ПРОГРАМИ")
    print("="*70)

if __name__ == "__main__":
    main()
