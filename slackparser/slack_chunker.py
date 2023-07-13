def time_based_chunker(seconds, data):
    chunked_data = []
    if len(data) == 0:
        return chunked_data
    
    last = data[0]["timestamp"].split('.')[0]
    metadata = []
    fulltext = ""
    for item in data:
        
        current = item["timestamp"].split('.')[0]

        if int(current) - int(last) > seconds:
            metadata.append(item)
            fulltext += " " + item["text"]
            chunked_data.append((metadata, fulltext))
            last = current
            fulltext = ""
            metadata = []
        else:
            metadata.append(item)
            fulltext += " " + item["text"]
            last = current
    
    chunked_data.append(("metadata", fulltext))



    return chunked_data

