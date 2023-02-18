import time

class dataFlow(object):
    def __init__(self):
        pass
    @classmethod
    def dataflow(cls, flowFunction, *args, **kwargs):
        # 紀錄當今時間(年月日時分秒)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 計算程式執行時間
        start = time.time()

        # 印出function名稱
        dataFlowAction = kwargs['dataFlowAction'] if 'dataFlowAction' in kwargs else 'dataFlowAction'
        dataFlowCommit = kwargs['dataFlowCommit'] if 'dataFlowCommit' in kwargs else 'dataFlowCommit'
        print(f'Time:{now}, dataFlowAction:{dataFlowAction}, dataFlowCommit:{dataFlowCommit}, '
              f'start run function:{flowFunction.__name__}...')
        obj = flowFunction(*args, **kwargs)

        # 計算程式執行時間
        end = time.time()
        hour = int((end - start) / 3600)
        min = int((end - start) / 60)
        sec = int((end - start) % 60)
        print(f'Time:{now}, end run function:{flowFunction.__name__}')
        print(f'time cost: {hour}h {min}m {sec}s\n')
        return obj

# 用工廠模式派生多個機器學習流程
class MLFlow(object):
    def __init__(self, mlFlowObject=None):
        self.mlFlowObject = mlFlowObject

    def __getattr__(self, name):
        # 印出self 的名稱
        print(f'__getattr__:{name}')
        def func_(*args, **kwargs):
            return dataFlow.dataflow(flowFunction=getattr(self.mlFlowObject, name), *args, **kwargs)
        return func_

    def __getattribute__(self, item):
        print(f'__getattribute__:{item}')
        return object.__getattribute__(self, item)
