import pandas as pd
import numpy as np
import pickle

import torch


# 前提假设：就两次规划结果
# contrast_path 比较动态规划的分段规划结果
# 判断2次规划[re plan点 -> end node]的路径是否相等
def contrast_path():
    plan_result = []
    f = open('./result/path.pkl', "rb")
    while 1:
        try:
            p = pickle.load(f)
            plan_result.append(p)
        except EOFError:
            break

    all_path = plan_result[0]
    re_path = plan_result[1]
    rePlan_node = re_path[0]
    index = all_path.index(rePlan_node)
    old_path = all_path[index:]
    print(old_path == re_path)


def find_high_variation():
    # 找到[T0, T1, T2]三个连续时间片，其中T0和T1 and T1和T2的差别较大。
    test = pd.read_pickle('./data_use/test_all.pkl')
    real_v_condition = test['x']
    time_num, _, link_num, _ = real_v_condition.shape

    # 设置一个阈值，表示速度差别较大的阈值
    # 测试时调整的参数（到3.5开始找不到符合的时间片了）
    threshold = 3.0
    high_variation = []

    # 遍历时间片，找到符合条件的三个连续时间片
    for t in range(time_num - 2):
        v_t0 = real_v_condition[t].squeeze()  # 当前时间片
        v_t1 = real_v_condition[t + 1].squeeze()  # 下一个时间片
        v_t2 = real_v_condition[t + 2].squeeze()  # 下下个时间片

        # 计算当前时间片和下一个时间片的速度差别
        diff_t0_t1 = np.mean(abs(v_t0 - v_t1))

        # 计算当前时间片和下下个时间片的速度差别
        diff_t1_t2 = np.mean(abs(v_t1 - v_t2))

        # 判断差别是否较大
        if diff_t0_t1 > threshold and diff_t1_t2 > threshold:
            high_variation.append(t)

    print(high_variation)  # [305, 2990, 2991, 4239] t=3.0


if __name__ == "__main__":
    # contrast_path()
    # find_high_variation()
    test = pd.read_pickle('./data_use/test_all.pkl')
    output = torch.load('./data_use/output_all.pth').numpy()  # 预测结果 (5795, 1, 6392, 1)
    now_t = 2990
    now_v = test['x']

    # real condition
    v_t0 = now_v[now_t].squeeze()  # 当前时间片T0
    v_t1 = now_v[now_t+1].squeeze()  # 下一个时间片T1
    v_t2 = now_v[now_t+2].squeeze()  # 下下个时间片T2

    # predict condition
    pre_v_t1 = output[now_t+1].squeeze()  # T1'
    pre_v_t2 = output[now_t+2].squeeze()  # T2'

    diff_t0_t1 = np.mean(abs(v_t0 - v_t1))
    diff_t1_t2 = np.mean(abs(v_t1 - v_t2))

    pre_diff_t1_t2 = np.mean(abs(pre_v_t1 - pre_v_t2))

    pre_now_t1 = np.mean(abs(v_t1 - pre_v_t1))
    pre_now_t2 = np.mean(abs(v_t2 - pre_v_t2))

    print('T0-T1:', diff_t0_t1)
    print('T1-T2:', diff_t1_t2)
    print("T1'-T2':", pre_diff_t1_t2)
    print("T1-T1':", pre_now_t1)
    print("T2-T2':", pre_now_t2)
