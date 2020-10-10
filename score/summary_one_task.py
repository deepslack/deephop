# --*-- coding: utf-8 --*--
# summary_one_task.py
# Copyright (c) 2020 Guangzhou fermion Technology Co.,Ltd. All rights reserved.
# create by aht  2020/7/8 上午10:32
from train import eval_test, TASKS
import os
import pandas as pd
import numpy as np

from util import find_best_model_checkpoint


def summary_multi_task():
    mt_dir = '/model/total_mtr'
    df = summary_one_dataset(mt_dir, TASKS)
    df.to_csv('/home/aht/paper_code/shaungjia/code/score/4次实验结果/mtdnn_.csv', index=False)


def summary_one_dataset(mt_dir, tasks_under_dir):
    df_list = []
    for s in range(3):
        model_save_dir = f'{mt_dir}/seed{s}'
        checkpoint = find_best_model_checkpoint(model_save_dir)
        print(f'use checkpoint {checkpoint}')
        df = eval_test(model_save_dir, checkpoint, tasks_under_dir)
        df_list.append(df)

    def apply_func(row):
        # target, r2, rmse = x
        target, r2, rmse = row['target'], row['r2'], row['rmse']
        r2_list = [r2]
        rmse_list = [rmse]
        for df in df_list[1:]:
            r2_list.append(df.loc[df.target == target, 'r2'].tolist()[0])
            rmse_list.append(df.loc[df.target == target, 'rmse'].tolist()[0])
        return np.mean(r2_list), np.std(r2_list), np.mean(rmse_list), np.std(rmse_list)

    df = df_list[0].copy(deep=True)
    df[['r2', 'r2_std', 'rmse', 'rmse_std']] = df.apply(apply_func, axis=1, result_type='expand')
    return df


def summary_per_task():
    base_dir = '/model/per_task'
    df_list = []
    for f in os.listdir(base_dir):
        df = summary_one_dataset(os.path.join(base_dir, f), [f[:-2]])
        df_list.append(df)
    total_df = pd.concat(df_list, axis=0)
    total_df.to_csv('/home/aht/paper_code/shaungjia/code/score/4次实验结果/mtdnn_per_task.csv', index=False)


if __name__ == '__main__':
    summary_multi_task()
    pass
