nums = [23, 7, 14, 2, 29, 11, 18, 5, 26, 8, 20, 13, 30, 1, 16, 24, 9, 4, 21, 27, 10, 3, 19, 6, 28, 15, 12, 22, 17, 25]
# nums = [5, 5, 6, 4, 10]
import time
import functools

def time_checker(func):
    @functools.wraps(func)
    def wrapper(nums, target):
        start_time = time.time()
        res = func(nums, target)
        finish_time = time.time()
        print(f"Решение функции {func.__name__} заняло {round(finish_time - start_time, 5)}")
        return res
    return wrapper



# решение №1
@time_checker
def twoSum1(nums, target):
    first_num = None
    second_num = None
    for num in nums:
        if target - num == num or num >= target:
            continue
        if not first_num:
            first_num = num
            continue

        if first_num + num == target:
            second_num = num
            break
    # теперь ищем индексы этих чисел
    res = [nums.index(first_num), nums.index(second_num)]
    print('Результат первого решения', res)
    return res
    

#решение №2
@time_checker
def twoSum2(nums, target):
    # отфильтруем числа которые меньше target
    filtered_nums = {num for num in nums if num < target}
    # print(filtered_nums)
    first_num = list(filtered_nums)[0]
    second_num = 0
    for num in list(filtered_nums)[1:]:
        if first_num + num == target:
            second_num = num
            break
    # теперь ищем индексы этих чисел
    res = [nums.index(first_num), nums.index(second_num)]
    print('Результат второго решения', res)
    return res


twoSum1(nums, 30)
twoSum2(nums, 30)