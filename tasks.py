from invoke import task

@task
def build_proto(ctx):

    src_dir = '/home/yichiuan/dev/python/python-serialization-benchmark/proto/'
    dst_dir = '/home/yichiuan/dev/python/python-serialization-benchmark/message/'

    inputs = ['addressbook', 'mydata']
    input_files = ''
    for input in inputs:
        input_files += src_dir + input + '.proto '

    cmd = "protoc -I={src_dir} --python_out={dst_dir} {input_files}".format(src_dir=src_dir,
                                                                            dst_dir=dst_dir,
                                                                            input_files=input_files)

    print('cmd : ' + cmd)
    ctx.run(cmd)

@task
def build_pyrobuf(ctx):

    src_dir = '/home/yichiuan/dev/python/python-serialization-benchmark/proto/'
    dst_dir = '/home/yichiuan/dev/python/python-serialization-benchmark/message_pyrobuf/'

    cmd = "pyrobuf --install {src_dir}".format(src_dir=src_dir)

    print('cmd : ' + cmd)
    ctx.run(cmd)
