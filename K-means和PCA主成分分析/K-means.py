# 当前版本 ： python3.8.2
# 开发时间 ： 2021/9/8 20:11
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
import matplotlib.colors as pltcolor


# ---------------------------part1.找到最邻近点---------------------------
def findCloseCenter(x, center):
    k, l = np.shape(center)  # k = 3, l = 2
    """
    numpy.tile()就是把数组沿各个方向复制
    tile 函数有两个参数 A 和 reps。
    tile这个函数是用来构造一个数组，内容按规则 reps (元组) 来重复参数 A (数组)。
    如果 reps 的长度是 d，那么生成结果的维度是 max(d,A.ndim)。A.ndim 表示参数 A 数组的维度。
    如果 A.ndim < d，那就在 A 的前面加上新的维度使其达到 d 维。
    如果 A.ndim > d，reps 就要在现有元素前面插入1，使它的长度达到 A.ndim。再对 A 进行重复。
    """
    xtemp = np.tile(x, k)  # (300, 6)
    centertemp = center.flatten()  # [3, 3, 6, 2, 8, 5] (6, )
    xtemp = np.power(xtemp-centertemp, 2)
    xt = np.zeros((np.size(xtemp, 0), k))
    for i in range(k):
        for j in range(l):
            xt[:, i] = xt[:, i]+xtemp[:, i*l+j]
    idx = np.argmin(xt, 1)+1
    return idx


print('Finding closest centroids.')
datainfo = scio.loadmat('ex7data2.mat')
X = datainfo['X']  # (300, 2)

K = 3
init_center = np.array([[3, 3], [6, 2], [8, 5]])
idX = findCloseCenter(X, init_center)
print('Closest centroids for the first 3 examples: ', idX[0:3])
print('(the closest centroids should be 1, 3, 2 respectively)')

# ---------------------------part2.计算均值---------------------------


# 找出中心点
def computeCenter(x, idx, k):
    m, n = np.shape(x)
    center = np.zeros((k, n))
    for i in range(k):
        pos = np.where(idx == i+1)
        center[i, :] = np.sum(x[pos], 0)/np.size(x[pos], 0)
    return center


print('Computing centroids means.')
center = computeCenter(X, idX, K)
print('Centroids computed after initial finding of closest centroids: ')
print(center)
print('the centroids should be: ')
print('[[ 2.428301 3.157924 ], [ 5.813503 2.633656 ], [ 7.119387 3.616684 ]]')
_ = input('Press [Enter] to continue.')

# =================== Part 3: K-Means Clustering ======================


# 中心点连线
def drawLine(p1, p2):
    x = np.array([p1[0], p2[0]])
    y = np.array([p1[1], p2[1]])
    plt.plot(x, y)


# 绘制数据点
def plotDataPoints(x, idx, k):
    colors = ['red', 'green', 'blue']
    plt.scatter(x[:, 0], x[:, 1], c=idx, cmap=pltcolor.ListedColormap(colors), s=40)


# 绘制中心点
def plotProgresskMeans(x, center, previous, idx, k, i):
    plotDataPoints(x, idx, k)
    plt.plot(center[:, 0], center[:, 1], 'x', ms=10, mew=1)
    for j in range(np.size(center, 0)):
        drawLine(center[j, :], previous[j, :])
    plt.title('Iteration number %d' % (i+1))


# k均值聚类
def runkMeans(x, init_center, max_iter, plot_progress=False):
    m, n = np.shape(x)
    k = np.size(init_center, 0)
    center = init_center
    previous_center = center
    idx = np.zeros((m,))

    if plot_progress:
        plt.ion()
        fig = plt.figure()

    for i in range(max_iter):
        print('K-Means iteration %d/%d...' % (i+1, max_iter))
        idx = findCloseCenter(x, center)
        if plot_progress:
            plotProgresskMeans(x, center, previous_center, idx, k, i)
            previous_center = center
            fig.canvas.draw()
            _ = input('Press [Enter] to continue.')
        center = computeCenter(x, idx, k)
    plt.show(block=True)
    plt.ioff()
    return center, idx


print('Running K-Means clustering on example dataset.')
max_iter = 10
K = 3
init_center = np.array([[3, 3], [6, 2], [8, 5]])
center, idx = runkMeans(X, init_center, max_iter, True)
print('K-Means Done.')


# ============= Part 4: K-Means Clustering on Pixels ===============
# 生成初始点
def kMeansInitCenter(x, k):
    randidx = np.random.permutation(np.size(x, 0))
    center = x[randidx[0: k], :]
    return center

print('Running K-Means clustering on pixels from an image.')
A = plt.imread('bird_small.png')
m, n, l = np.shape(A)
A_x = np.reshape(A, (m*n, l))
A_k = 16
A_max_iter = 10
A_init_center = kMeansInitCenter(A_x, A_k)
A_center, A_idx = runkMeans(A_x, A_init_center, A_max_iter)
print(A_center)


# ================= Part 5: Image Compression ======================
print('Applying K-Means to compress an image.')
A_idx = findCloseCenter(A_x, A_center)
X_recovered = A_center[A_idx-1, :]
X_back = X_recovered.reshape(m, n, l)
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.imshow(A)
ax1.set_title('Original')
ax2 = fig.add_subplot(122)
ax2.imshow(X_back)
ax2.set_title('Compressed, with %d colors.' % A_k)
plt.show(block=False)