import tensorflow as tf
import input
import model

filenames, labels = input.get_filenames_labels(12500, .8, True, "../train_processed")

x, y_ = input.input_pipeline(filenames, labels, 20)


sess = tf.Session()

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

logs_path = "../logs"
summary_writer = tf.train.SummaryWriter(logs_path, graph=tf.get_default_graph())

y = model.model(x)
loss = model.get_loss(y, y_)
optimizer =model.get_optimizer(loss)

merged_summary_op = model.get_summary_op(x, loss)

saver = tf.train.Saver()

saver.restore(sess, "../saved_models/model.ckpt")

sess.run(tf.global_variables_initializer())

i = 0
try:
    while not coord.should_stop() and i < 100000:
        _, summary = sess.run([optimizer, merged_summary_op])
        # print(x.eval(session=sess))

        if i % 1000 == 0:
            summary_writer.add_summary(summary, i)

        if i % 10000 == 0:
            save_path = saver.save(sess, "../saved_models/model.ckpt")

        i += 1

except tf.errors.OutOfRangeError:
    print("Done")
finally:
    coord.request_stop()

coord.join(threads)

sess.close()