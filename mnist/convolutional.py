import os
import mnist.model as model
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

'''训练卷积神经网络'''

data = input_data.read_data_sets("./MNIST_data/", one_hot=True)

# model
with tf.variable_scope("convolutional"):
    x = tf.placeholder(tf.float32, [None, 784])
    #解决过拟合问题
    keep_prob = tf.placeholder(tf.float32)
    y, variables = model.convolutional(x, keep_prob)

# train
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
#AdamOptimizer 数据量大，比梯度下降算法要快些
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
'''
tf.argmax(input, axis=None, name=None, dimension=None)
此函数是对矩阵按行或列计算最大值

参数
input：输入Tensor
axis：0表示按列，1表示按行
name：名称
dimension：和axis功能一样，默认axis取值优先。新加的字段
'''
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver(variables)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(500):
        batch = data.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels, keep_prob: 1.0}))

    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__), 'data', 'convolutional.ckpt'),
        write_meta_graph=False, write_state=False)
    print("Saved:", path)
