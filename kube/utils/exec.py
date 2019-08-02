import subprocess

class EXEC:

    def sh(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            print(output)
        except subprocess.CalledProcessError as err:
            print(err.output)
            raise
        return str(output.strip(), 'utf-8')
