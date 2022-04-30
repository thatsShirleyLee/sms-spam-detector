from matplotlib import pyplot as plt
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_recall_fscore_support, plot_roc_curve, \
    plot_confusion_matrix
import joblib

# 拟合分类器并返回指标
from sklearn.model_selection import train_test_split


def train_test_clf(clf, X_train, y_train, X_test, y_test, tag="", isShow=False):
    """
    Args:
        clf:     分类器对象
        X_train: 训练数据编码值
        y_train: 训练数据标签
        X_test:  测试数据编码值
        y_test:  测试数据标签
        tag: 字符串（编码器和分类器）
        isShow: 是否画图
    """
    # 拟合分类器
    clf.fit(X_train, y_train)
    joblib.dump(clf, r'D:\GraduationDesign\sms-spam-detector\saved_model\{}.joblib'.format(type(clf).__name__))
    y_pred = clf.predict(X_test)

    # 计算分类器评估值
    acc = accuracy_score(y_test, y_pred)
    bacc = balanced_accuracy_score(y_test, y_pred)
    prec, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', pos_label=1)

    # 打印评估值
    print('{:<36s} Balanced accuracy: {:.2f}%'.format(tag, bacc * 100))
    if isShow:
        # CalibrationDisplay.from_estimator(clf, X_test, y_test)
        # plt.show()
        plot_confusion_matrix(clf, X_test, y_test)
        # plot_roc_curve(clf, X_test, y_test)
    return acc, bacc, prec, recall, f1



