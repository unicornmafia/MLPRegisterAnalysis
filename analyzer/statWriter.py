
class StatWriter:
    def __init__(self, output_file, diff_file, file_stats, group_stats):
        self.output_file = output_file
        self.diff_file = diff_file
        self.file_stats = file_stats
        self.group_stats = group_stats

    def get_output_header_line(self, sorted_tags):
        output_line = "File Name, Num Words, Num Tokens, Num Sentences, Num Speakers, Ave Sentence Len, Ave Word Len"
        for tag in sorted_tags:
            #  oops.  csv logic error.  >_<
            output_line += ", " + tag
        return output_line

    def output_analysis(self, sorted_tags):
        sorted_files = sorted(self.file_stats.keys())
        sorted_groups = sorted(self.group_stats.keys())

        # write the header
        header_line = self.get_output_header_line(sorted_tags)
        print(header_line)
        self.output_file.write(header_line + "\n")

        # write a row for each file
        for file in sorted_files:
            output_line = self.file_stats[file].get_output_line(sorted_tags)
            print(output_line)
            self.output_file.write(output_line + "\n")

        # write a row for each group
        self.output_file.write("\n")
        for group in sorted_groups:
            output_line = self.group_stats[group].get_output_line(sorted_tags)
            print(output_line)
            self.output_file.write(output_line + "\n")

        # write a normalized row for each group
        self.output_file.write("\n")
        for group in sorted_groups:
            output_line = self.group_stats[group].get_normalized_output_line(sorted_tags, 1000)
            print(output_line)
            self.output_file.write(output_line + "\n")

    def get_stat_diff(self, group1_stats, group2_stats):
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

    def write_differences(self, name, sorted_differences):
        self.diff_file.write("\nMost Significant Differences for: " + name + "\n")
        self.diff_file.write("Feature, Min, Max, Diff, % change\n")
        for triple in sorted_differences:
            self.diff_file.write(triple[0] + ", " +
                            str(round(triple[1], 2)) + ", " +
                            str(round(triple[2], 2)) + ", " +
                            str(round(triple[3], 2)) + ", " +
                            str(round(triple[4], 2)) + "\n")

    def output_most_significant_differences_between_groups(self, group1, group2, sorted_tags):
        group1_stats = self.group_stats[group1].get_normalized_output_stat_set(sorted_tags, 1000)
        group2_stats = self.group_stats[group2].get_normalized_output_stat_set(sorted_tags, 1000)

        # first print group1's in order
        differences1 = self.get_stat_diff(group1_stats, group2_stats)
        sorted_differences1 = sorted(differences1, key=lambda x: x[4], reverse=True)
        self.write_differences(self.group_stats[group2].file_name, sorted_differences1)

        # then print group2's in order
        differences2 = self.get_stat_diff(group2_stats, group1_stats)
        sorted_differences2 = sorted(differences2, key=lambda x: x[4], reverse=True)
        self.write_differences(self.group_stats[group1].file_name, sorted_differences2)