import sys
from sortedcontainers import SortedSet

# input arguments
season = sys.argv[1]
episode = sys.argv[2]
name = sys.argv[3]

# file formats should be like:
# mlpaf-s1e4-raw-dialog-brightlights.txt process.py
# mlpaf-s1e4-dialog-brightlights.txt
# mlpaf-s1e4-speakers-unique-brightlights.txt

inputFileName = "mlpaf-s{}e{}-raw-dialog-{}.txt".format(season, episode, name)
dialogOutputFileName = "mlpaf-s{}e{}-dialog-{}.txt".format(season, episode, name)
speakersOutputFileName = "mlpaf-s{}e{}-speakers-unique-{}.txt".format(season, episode, name)

print("Processing...")
print("Input File: " + inputFileName)
print("Dialog Output File: " + dialogOutputFileName)
print("Speakers Output File: " + speakersOutputFileName + "\n")

inputFile = open(inputFileName)
dialogOutputFile = open(dialogOutputFileName, "w")
speakersOutputFile = open(speakersOutputFileName, "w")

speaker = ""
dialog = ""

speakers = set()


def add_speakers(speaker_attribution):
    coordianted_string = speaker_attribution.split("and")
    for coordinate_element in coordianted_string:
        trimmed_coordinate_element = coordinate_element.strip()
        if trimmed_coordinate_element != "":
            comma_list = trimmed_coordinate_element.split(",")
            for element in comma_list:
                trimmed_element = element.strip("?")
                trimmed_element = trimmed_element.strip()
                if trimmed_element != "":
                    speakers.add(trimmed_element)


def write_speakers():
    sorted_speakers = SortedSet(speakers)
    for sorted_speaker in sorted_speakers:
        if sorted_speaker != "?":
            speakersOutputFile.write(sorted_speaker + "\n")


def write_dialog():
    if dialog != "":
        processed_dialog = dialog.replace("\n", " ").strip()
        if processed_dialog != "":
            dialogOutputFile.write(processed_dialog + "\n")


def write_to_output_files():
    print(speaker)
    add_speakers(speaker)
    write_dialog()

for line in inputFile:
    line = line.strip()
    if line != "" and line[0] == "[":
        rightOffset = line.find("]")
        if rightOffset != -1 and rightOffset < len(line):
            write_to_output_files()  # write the old one
            speaker = line[1:rightOffset].strip()
            dialog = line[rightOffset+1:len(line)].strip()
    else:
        dialog += "  " + line

write_dialog()  # write the last one

# write the speakers file
write_speakers()

# close files
speakersOutputFile.close()
dialogOutputFile.close()
inputFile.close()



