from operator import itemgetter


def two_list_merge(tag1, tag2, stream1, stream2):
    stream = []
    stream.extend([(tag1, element) for element in stream1])
    stream.extend([(tag2, element) for element in stream2])

    stream.sort(key=itemgetter(1))
    return stream
