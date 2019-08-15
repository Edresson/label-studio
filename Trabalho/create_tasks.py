import argparse
import os
import json
import warnings


def check_args(args):
    corpus = os.path.abspath(args.corpus)
    output = os.path.abspath(args.output) if args.output else ''
    if not os.path.exists(args.corpus):
        raise FileNotFoundError(
            'No such file or directory: \'{}\''.format(corpus))
    if not os.path.isdir(args.corpus):
        raise ValueError('Path \'{}\' is not a directory'.format(corpus))
    if output:
        if not os.path.exists(output):
            raise FileNotFoundError(
                'No such file or directory \'{}\''.format(output))
        if not os.path.isdir(output):
            raise ValueError('Path \'{}\' is not a directory'.format(output))
    return corpus, output


def main(corpus, output):
    texts = list()
    for filename in os.listdir(corpus):
        filepath = os.path.join(corpus, filename)
        if os.path.isfile(filepath):
            with open(os.path.join(corpus, filename)) as file_:
                texts.append({'text': file_.read()})
        else:
            w = 'Ignoring directory: \'{}\''.format(filename)
            warnings.warn(w, RuntimeWarning)

    if not texts:
        raise ValueError('No files in the given corpus: \'{}\''.format(corpus))
    tasks = json.dumps(texts)
    savepath = os.path.join(output, 'tasks.json')
    with open(savepath, 'w') as tasks_file:
        tasks_file.write(tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', '-c', type=str,
                        required=True,
                        help='Corpus path')
    parser.add_argument('--output', '-o', type=str,
                        required=False,
                        help='Output path')
    ARGS = parser.parse_args()
    corpus, output = check_args(ARGS)
    main(corpus, output)
