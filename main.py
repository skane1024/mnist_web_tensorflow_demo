import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request

from mnist import model

print(tf.__version__)

x = tf.placeholder("float", [None, 784])
sess = tf.Session()

# restore trained data
with tf.variable_scope("regression"):
    y1, variables = model.regression(x)
saver = tf.train.Saver(variables)
saver.restore(sess, "mnist/data/regression.ckpt")


with tf.variable_scope("convolutional"):
    keep_prob = tf.placeholder("float")
    y2, variables = model.convolutional(x, keep_prob)
saver = tf.train.Saver(variables)
saver.restore(sess, "mnist/data/convolutional.ckpt")


def regression(input):
    return sess.run(y1, feed_dict={x: input}).flatten().tolist()


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


# webapp
app = Flask(__name__)

'''
request.json
一维数组，784个特征
[255, 161, 0, 0,....]
'''
@app.route('/api/mnist', methods=['POST'])
def mnist():
    #标准化数据
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    #一维数组，输出10个预测概率
    output1 = regression(input)
    output2 = convolutional(input)
    return jsonify(results=[output1, output2])

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
