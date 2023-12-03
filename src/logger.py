import json
import hashlib
import os


class Logger:
    log_file = None

    @classmethod
    def set_log_file(cls, log_file):
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            open(log_file, 'w').close()  # Create the file if it doesn't exist

        cls.log_file = log_file

    @classmethod
    def _hash_text(cls, text):
        return hashlib.sha256(text.encode()).hexdigest()

    @classmethod
    def _load_logs(cls):
        try:
            with open(cls.log_file, 'r') as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = {}
        return logs

    @classmethod
    def _save_logs(cls, logs):
        with open(cls.log_file, 'w') as file:
            json.dump(logs, file, indent=4)

    @classmethod
    def _log_message(cls, level, message):
        if level == 'print':
            print(message)
        else:
            logs = cls._load_logs()
            hash_key = cls._hash_text(message)

            if hash_key in logs and logs[hash_key]['ignore']:
                return

            print(message)

            logs[hash_key] = {'text': message, 'ignore': False}
            cls._save_logs(logs)

    @classmethod
    def print(cls, message):
        cls._log_message('print', message)

    @classmethod
    def warn(cls, message):
        cls._log_message('warn', f'\033[93m{message}\033[0m')

    @classmethod
    def error(cls, message):
        cls._log_message('error', f'\033[91m{message}\033[0m')

    @classmethod
    def cleanup_logs(cls):
        # remove all entries that are set to ignore false
        logs = cls._load_logs()
        for key in list(logs.keys()):
            if not logs[key]['ignore']:
                del logs[key]
        cls._save_logs(logs)


if __name__ == '__main__':
    # clean up logs
    Logger.set_log_file('../data/log.json')
    Logger.cleanup_logs()
