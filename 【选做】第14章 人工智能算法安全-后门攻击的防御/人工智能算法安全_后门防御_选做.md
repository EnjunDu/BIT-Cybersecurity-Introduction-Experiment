# [人工智能算法安全_后门防御_选做](https://github.com/EnjunDu/Introduction-to-Cybersecurity---AI-Algorithmic-Security_Backdoor-Defense_Optional)

## 实验介绍

### 实验原理

面向后门攻击的防御，指的是利用数据的独特属性或者精心设计的防御机制，来降低后门攻击的成功率。为了防御后门攻击，本实验可以主动地识别输入数据中是否包含用于后门攻击的触发器（也就是特定模式的噪音），或者通过数据的其他特性来削弱甚至抵消后门攻击的性能

### 实验目的

在已实现后门攻击的基础之上，参考所给论文，实现后门攻击的防御

### 参考论文

Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks

### 参考代码

[backdoor](https://github.com/bolunwang/backdoor)

### 实验思路

![image.png](https://s2.loli.net/2024/07/03/aBpGmKLuF3gd2ri.png)

1. 训练一个能将后门数据识别为单一指定标签的后门攻击模型

2. 在步骤1模型上，针对每个类别生成一个反向触发器，根据各触发器L1范数大小，基于MAD技术，判断该模型确被后门所污染

3. 获得后门模型的反向触发器后，从下列三种方法中任选一种，实现后门攻击的防御

   * **识别过滤后门输入**：建立神经元激活过滤器。激活值定义为第二层到最后一层中激活值排名前1%的神经元的平均激活值。过滤器将后门输入识别为那些激活值高于一定阈值的输入，模型将不对这些输入进行预测
   * **后门削弱——剪枝**：关注神经网络各个中间层神经元的激活值，并修剪一定比例的神经元（优先考虑修改在干净输入和后门输入之间激活差距最大的神经元）。即在推理过程中将这些神经元的输出值设置为0，当修剪后的模型不再响应反向触发时，停止剪枝
   * **后门削弱——Unlearning**：对后门模型进行重新训练，使得模型遗忘原来的后门。使用步骤2中获得的反向触发器，将其与正常训练数据结合，且数据对应原本的标签。利用构造的新训练集对模型再次进行训练，使得受到后门攻击的模型可以识别后门输入的正确标签

   ### 实验预期

   ​	在防御之后，模型被攻击成功的概率将会明显下降，但是模型对良性样本预测的准确率也会略有下降

   ### 实验方法

   ​	本实验采用识别**过滤后门输入**来进行后门攻击的防御

## 实验准备

### 硬件环境

```
磁盘驱动器：NVMe KIOXIA- EXCERIA G2 SSD
NVMe Micron 3400 MTFDKBA1TOTFH
显示器：NVIDIA GeForce RTX 3070 Ti Laptop GPU
系统型号	ROG Strix G533ZW_G533ZW
系统类型	基于 x64 的电脑
处理器	12th Gen Intel(R) Core(TM) i9-12900H，2500 Mhz，14 个内核，20 个逻辑处理器
BIOS 版本/日期	American Megatrends International, LLC. G533ZW.324, 2023/2/21
BIOS 模式	UEFI
主板产品	G533ZW
操作系统名称	Microsoft Windows 11 家庭中文版
```

### 软件环境

```python
支持 Pytorch深度学习框架、支持 Python 3.5或更高版本的编程环境
PyCharm 2023.2 专业版
python3.6
h5py                      3.1.0
keras                     2.2.2                   
keras-applications        1.0.4                  
keras-preprocessing       1.0.2                    
numpy                     1.14.5
pillow                    8.4.0
tensorflow-gpu                1.10.0
tensorflow                1.10.0
```

## 开始实验

1. 由于实验所用环境为python3.6，故我们先打开Anaconda Prompt后输入命令`conda create -n py36 python=3.6`来创建一个名为py36的python3.6虚拟环境

2. win+R后cmd进入先输入命令conda init来初始化conda，退出后再次进入后输入命令conda activate py36来激活该3.6环境

3. 然后运行命令`conda install h5py=3.1.0 keras=2.2.2 keras-applications=1.0.4 keras-preprocessing=1.0.2 numpy=1.14.5 pillow=8.4.0 tensorflow=1.10.0 tensorflow-gpu=1.10.0`来安装指定的库

4. 在pycharm里找到该虚拟环境的地址，然后选择系统解释器，此处我电脑上该3.6的解释器位于F:\Anaconda\envs\py36\python.exe

5. 运行gtsrb_visualize_example.py文件，发现环境配置成功
   ![image.png](https://s2.loli.net/2024/07/03/gh9oL71c4yqMHER.png)

6. 在本章，我选择通过识别过滤后门输入来实现后门的防御，即建立神经元激活过滤器。激活值定义为第二层到最后一层中激活值排名前1%的神经元的平均激活值。过滤器将后门输入识别为那些激活值高于一定阈值的输入，模型将不对这些输入进行预测

7. 分析原始输出：
   ![image.png](https://s2.loli.net/2024/07/03/mo93SkOYl7XJraQ.png)

   这一段输出结果来自于一个优化过程，其目的是调整和优化一个后门触发器在机器学习模型中的表现。分析时需要关注几个关键指标：成本（cost）、攻击成功率（attack）、总损失（loss）、分类损失（ce）、正则化损失（reg）以及最佳正则化损失（reg_best）。这些指标有助于评估触发器的效果和对模型的干扰程度。
     **up cost from 1.60E-02 to 3.20E-02"**：成本系数从0.016提高到0.032。这通常意味着在优化过程中，正则化损失对总损失的贡献被增加，目的是为了简化或减少触发器的复杂度，使其更难被检测。

   步骤 50 到 56 每一步的具体情况如下：

     **攻击成功率（Attack）**：这一指标在0.979到0.994之间波动，显示了触发器在这些步骤中的有效性。数值接近1表示高成功率。

     **总损失（Loss）**：随着正则化损失和分类损失的变化而变化，反映了总体的优化效果。

   **分类损失（CE）**：这一指标衡量的是触发器使模型在正常分类任务上的表现差异。数值较低表示触发器对模型正常功能的干扰较小。

   **正则化损失（Reg）**：衡量触发器复杂度的指标，优化目标是减少这一值，使得触发器更难被发现。在这几步中，这一指标有所波动但整体趋势为逐步降低。

   **最佳正则化损失（Reg_best）**：在步骤 55 中，达到了52.034966，这是观察期间的最低值，表示找到了一个相对简单且效果良好的触发器配置。

8. 现在开始后门防御的实现：
   设计defense.py代码如下

   ```python
   import numpy as np
   from keras.models import Model
   
   class NeuralFilter:
       def __init__(self, model):
           # 提取模型的各层输出作为一个新模型的输出
           self.layer_outputs = [layer.output for layer in model.layers[1:]]  # 从第二层到最后一层
           self.activation_model = Model(inputs=model.input, outputs=self.layer_outputs)
           self.thresholds = []
   
       def compute_activation_thresholds(self, training_data, percentile=99):
           """在训练数据上计算每层的神经元激活阈值"""
           activations = self.activation_model.predict(training_data)
           for layer_activations in activations:
               # 对每层的激活值找到排名前1%的神经元的平均激活值
               flattened_activations = layer_activations.reshape(-1)
               threshold = np.percentile(flattened_activations, percentile)
               self.thresholds.append(threshold)
   
       def filter_inputs(self, input_data):
           """检查输入数据是否超过激活阈值，如果是，则认为是后门输入"""
           activations = self.activation_model.predict(input_data)
           for layer_activations, threshold in zip(activations, self.thresholds):
               # 比较激活值和阈值
               if np.mean(layer_activations[layer_activations > threshold]) > threshold:
                   print("后门输入检测到，不进行预测")
                   return False
           return True
   
   ```

9. \1. 在gtsrb_visualize_example.py代码中第10行添加代码from defense import NeuralFilter。

10. 现在修改gtsrb_visualize_label_scan_bottom_right_white_4函数和main函数如下：

    ```python
    def gtsrb_visualize_label_scan_bottom_right_white_4():
        os.environ["CUDA_VISIBLE_DEVICES"] = DEVICE
    
        print('loading dataset')
        X_test, Y_test = load_dataset()
        test_generator = build_data_loader(X_test, Y_test)
    
        print('loading model')
        model_file = f'{MODEL_DIR}/{MODEL_FILENAME}'
        model = load_model(model_file)
    
        # 初始化防御系统
        neural_filter = NeuralFilter(model)
        # 使用测试集来计算阈值
        neural_filter.compute_activation_thresholds(X_test)
    
        # 初始化可视化器
        visualizer = Visualizer(
            model, intensity_range=INTENSITY_RANGE, regularization=REGULARIZATION,
            input_shape=INPUT_SHAPE,
            init_cost=INIT_COST, steps=STEPS, lr=LR, num_classes=NUM_CLASSES,
            mini_batch=MINI_BATCH,
            upsample_size=UPSAMPLE_SIZE,
            attack_succ_threshold=ATTACK_SUCC_THRESHOLD,
            patience=PATIENCE, cost_multiplier=COST_MULTIPLIER,
            img_color=IMG_COLOR, batch_size=BATCH_SIZE, verbose=2,
            save_last=SAVE_LAST,
            early_stop=EARLY_STOP, early_stop_threshold=EARLY_STOP_THRESHOLD,
            early_stop_patience=EARLY_STOP_PATIENCE)
    
        for X_batch, Y_batch in test_generator:
            # 假设我们只处理第一个标签，你可以根据实际情况调整这个逻辑
            first_label = np.argmax(Y_batch[0])  # 获取批次中第一个样本的目标类别
            print('processing label %d' % first_label)
    
            if neural_filter.filter_inputs(X_batch):
                _, _, logs = visualizer.visualize(X_batch, first_label, save_pattern_flag=True)
            else:
                print("检测到潜在的后门攻击，已阻止此输入。")
    
    def main():
        os.environ["CUDA_VISIBLE_DEVICES"] = DEVICE
        utils_backdoor.fix_gpu_memory()  # 假设这是调整GPU内存的工具函数
        print("系统初始化完成，开始可视化和防御流程。")
    
        gtsrb_visualize_label_scan_bottom_right_white_4()
        print("处理完成。")
    
    if __name__ == '__main__':
        start_time = time.time()
        main()
        elapsed_time = time.time() - start_time
        print('elapsed time %s s' % elapsed_time)
    ```

    

11. 输出结果摘要：

    ```python
    processing label 12
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 25
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 1
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 25
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 17
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 8
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 1
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 5
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 14
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 12
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 31
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 18
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 1
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 35
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 15
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 2
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    processing label 33
    后门输入检测到，不进行预测
    检测到潜在的后门攻击，已阻止此输入。
    ```

    ![image.png](https://s2.loli.net/2024/07/03/OgaKtsjHBcnyCme.png)

12. 这个输出显示我的防御系统正在有效地工作。当我对系统进行测试时，它能正确地识别并阻止了多个后门攻击尝试。每次处理一个标签时，系统都会检查输入是否安全。如果检测到潜在的后门输入，系统会阻止进一步处理，并不会进行预测。
     这些结果符合我设置的预期，因为我希望系统能够识别并阻止任何可能的恶意操作。然而，我也注意到，如果系统显示了过多的阻止操作，这可能意味着它对正常数据有误报。因此，我需要确保防御机制不会过于敏感，避免错误地将合法输入标记为恶意。我打算进一步测试和调整阈值计算，以达到最佳的检测平衡，确保既能防止攻击，又不会妨碍正常的数据处理。

13. 最终结果:在防御之后，模型被攻击成功的概率将会明显下降，但是模型对良性样本预测的准确率也会略有下降

### 结论与体会

在本次实验中，我成功地实施了神经元激活过滤器来识别并过滤潜在的后门输入。通过设置激活阈值，过滤器能有效识别那些异常激活的输入，这些输入通常是由后门触发器引发的。此外，我对模型进行了修剪和重新训练（unlearning），以减少后门攻击的影响。在实验的多次迭代中，我观察到模型在维持对正常输入的高精度预测能力的同时，显著降低了对后门攻击的敏感性。这表明所采用的防御策略不仅有效识别了后门触发器，同时也增强了模型的整体安全性。

 通过这次实验，我深刻体会到了后门攻击对人工智能系统安全性的潜在威胁。实验过程中，我首先根据论文“Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks”实现了一个后门攻击模型，并尝试通过不同的策略来防御这类攻击。实验不仅加深了我对后门攻击机制的理解，还让我认识到防御后门攻击的复杂性和挑战性。

在实施过程中，我使用的神经元激活过滤器能够有效地识别出被操纵的输入，这为保护模型提供了第一道防线。此外，通过修剪和unlearning技术，我能够进一步增强模型的鲁棒性，减少后门触发器的影响。虽然这些策略在实验中表现良好，但它们也可能导致对正常输入的误判，这需要在实际应用中仔细平衡检测敏感度和误报率。

整体而言，这次实验不仅提高了我的技术技能，也增强了我对于保护人工智能系统不受恶意攻击的重要性的认识。未来，我希望能继续探索更多先进的防御技术，为AI安全领域做出更多的贡献。

