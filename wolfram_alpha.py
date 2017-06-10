import wolframalpha

import config

wolframalphaClient = wolframalpha.Client(config.wa_token)


def query_wa(args):
    a = wolframalphaClient.query(args)
    array = []
    for pod in a.pods:
        if pod.text is not None:
            string = ""
            string += "*" + pod.title + "*\n"
            string += '`' + pod.text + '`'
            array.append(string)
    m = "\n\n".join(array)
    if not m:
        return "Error processing input"
    return m
