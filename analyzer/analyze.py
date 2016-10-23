import glob
import nltk
from nltk import word_tokenize
from textStats import TextStats
from nltk.tokenize import sent_tokenize

#
# set up variables
#
output_file_name = "mlp_analysis.csv"
output_file = open(output_file_name, "w")

diff_file_name = "stat_diffs.csv"
diff_file = open(diff_file_name, "w")

print("Output File: " + output_file_name + "\n")

files = glob.glob("*-dialog-*.txt")
sorted_files = sorted(files)

all_tags = set()
file_stats = dict()
group_stats = dict()


def add_tuple(tuple, file_name, group_name):
    # keep track of all tags
    tag = tuple[1]
    if tag == ",":
        tag = "comma"

    all_tags.add(tag)

    # add to file stats
    if file_name not in file_stats:
        file_stats[file_name] = TextStats(file_name)
    file_stats[file_name].add_tuple(tuple)

    # add to group stats
    if group_name not in group_stats:
        group_stats[group_name] = TextStats(group_name)
    group_stats[group_name].add_tuple(tuple)


def add_sentence(sentence, file_name, group_name):
    # add to file stats
    if file_name not in file_stats:
        file_stats[file_name] = TextStats(file_name)
    file_stats[file_name].add_sentence(sentence)

    # add to group stats
    if group_name not in group_stats:
        group_stats[group_name] = TextStats(group_name)
    group_stats[group_name].add_sentence(sentence)


def analyze_file(file_name, group_name):
    input_file = open(file_name)
    for line in input_file:
        sentences = sent_tokenize(line)
        tokens = word_tokenize(line)
        pos_tags = nltk.pos_tag(tokens)
        for tuple in pos_tags:
            add_tuple(tuple, file_name, group_name)

        for sentence in sentences:
            add_sentence(sentence, file_name, group_name)

        print(str(pos_tags))


def get_output_header_line(sorted_tags):
    output_line = "File Name, Num Words, Num Tokens, Num Sentences, Ave Sentence Len, Ave Word Len"
    for tag in sorted_tags:
        #  oops.  csv logic error.  >_<
        output_line += ", " + tag
    return output_line


def output_analysis(sorted_tags):
    sorted_files = sorted(file_stats.keys())
    sorted_groups = sorted(group_stats.keys())

    # write the header
    header_line = get_output_header_line(sorted_tags)
    print(header_line)
    output_file.write(header_line + "\n")

    # write a row for each file
    for file in sorted_files:
        output_line = file_stats[file].get_output_line(sorted_tags)
        print(output_line)
        output_file.write(output_line + "\n")

    # write a row for each group
    output_file.write("\n")
    for group in sorted_groups:
        output_line = group_stats[group].get_output_line(sorted_tags)
        print(output_line)
        output_file.write(output_line + "\n")

    # write a normalized row for each group
    output_file.write("\n")
    for group in sorted_groups:
        output_line = group_stats[group].get_normalized_output_line(sorted_tags, 1000)
        print(output_line)
        output_file.write(output_line + "\n")


def get_stat_diff(group1_stats, group2_stats):
    sig_percent_cutoff = 2.0
    sig_value_cutoff = 10.0
    diffs = list()
    for i in range(0, len(group1_stats)):
        tuple1 = group1_stats[i]
        stat_name1 = tuple1[0]
        stat_value1 = tuple1[1]
        tuple2 = group2_stats[i]
        stat_name2 = tuple2[0]
        stat_value2 = tuple2[1]
        if stat_name1 != stat_name2:
            raise Exception("Stat values do not compare")
        diff = stat_value2 - stat_value1
        if stat_value1 != 0:
            percent_change = diff/stat_value1 * 100
        else:
            percent_change = 0
        if percent_change > sig_percent_cutoff and (stat_value1 >= sig_value_cutoff or stat_value2 >= sig_value_cutoff):
            diffs.append((stat_name1, stat_value1, stat_value2, diff, percent_change))
    return diffs


def write_differences(name, sorted_differences):
    diff_file.write("\nMost Significant Differences for: " + name + "\n")
    diff_file.write("Feature, Min, Max, Diff, % change\n")
    for triple in sorted_differences:
        diff_file.write(triple[0] + ", " +
                        str(round(triple[1], 2)) + ", " +
                        str(round(triple[2], 2)) + ", " +
                        str(round(triple[3], 2)) + ", " +
                        str(round(triple[4], 2)) + "\n")


def output_most_significant_differences_between_groups(group1, group2, sorted_tags):
    group1_stats = group_stats[group1].get_normalized_output_stat_set(sorted_tags, 1000)
    group2_stats = group_stats[group2].get_normalized_output_stat_set(sorted_tags, 1000)

    # first print group1's in order
    differences1 = get_stat_diff(group1_stats, group2_stats)
    sorted_differences1 = sorted(differences1, key=lambda x: x[4], reverse=True)
    write_differences(group_stats[group2].file_name, sorted_differences1)

    # then print group2's in order
    differences2 = get_stat_diff(group2_stats, group1_stats)
    sorted_differences2 = sorted(differences2, key=lambda x: x[4], reverse=True)
    write_differences(group_stats[group1].file_name, sorted_differences2)


def get_group_name_from_file_name(file_name):
    parts = file_name.split("-")
    return parts[0]


def add_speakers(file_name, group_name):
    speakers_file_name = file_name.replace("-dialog-", "-speakers-unique-")
    speakers_file = open(speakers_file_name)
    for line in speakers_file:
        speaker = line.strip().lower()
        if speaker != "and":
            group_stats[group_name].add_speaker(speaker)
            file_stats[file_name].add_speaker(speaker)

#
# START HERE
#
for file_name in sorted_files:
    print("\nAnalyzing: " + file_name)
    group_name = get_group_name_from_file_name(file_name)
    analyze_file(file_name, group_name)
    add_speakers(file_name, group_name)

sorted_tags = sorted(all_tags)
output_analysis(sorted_tags)
output_most_significant_differences_between_groups("mlpaf", "mlpfim", sorted_tags)
output_file.close()
diff_file.close()
