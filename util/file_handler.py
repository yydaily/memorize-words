import os
class file_handler():
    def __init__(self, path):
        self.path_ = path
        if not os.path.exists(path):
            os.makedirs(path)

    def wrap_list_to_file(self, file_name, l):
        with open(self.path_ + '/' + file_name, 'w+') as f:
            f.write(';'.join(map(str, l)))

    def unwrap_list_from_file(self, file_name):
        with open(self.path_ + '/' + file_name, 'r') as f:
            return list(f.readline().split(';'))

    def write_file(self, file_name, data, write_mode):
        with open(self.path_ + '/' + file_name, write_mode) as f:
            f.write(data)

    def remove_file(self, file_name):
        if os.path.exists(self.path_ + '/' + file_name):
            os.remove(self.path_ + '/' + file_name)

if __name__ == '__main__':
    fh = file_handler('.')
    fh.wrap_list_to_file('test', [1, 2,3])
    print(fh.unwrap_list_from_file('test'))
