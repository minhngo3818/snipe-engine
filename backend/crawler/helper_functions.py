#filters the dictionary to only contain if the frequency is 1 and returns number
def find_unique_urls(dict):
    unique_items = {key: value for key, value in dict.items() if value == 1}
    return len(unique_items.keys())
    # with open("reportTask1.json", "w") as json_file:
    #     json.load(json_file)
    #     json.dump(unique_items.keys(), json_file)

#prints number of subdomains in uci.ics.edu and sorts alphabetically
def sort_subdomains(dict):
    print(len(dict.keys()))
    return {key: dict[key] for key in sorted(dict.keys())}
