import language_check
from langdetect import detect
from typing import List, Tuple

Match = language_check.Match
Matches = List[Match]


def print_error(matches: Matches, i: int) -> None:
    error = matches[i]
    print('-------------------')
    print('Rule ID: ', error.ruleId)
    print('Category: ', error.category)
    print('Error and context: ', error.context)
    print(error.msg)


def print_errors(matches: Matches) -> None:
    for i in range(len(matches)):
        error = matches[i]
        print('-------------------')
        print('Rule ID: ', error.ruleId)
        print('Category: ', error.category)
        print('Error and context: ', error.context)
        print(error.msg)


def manage_errors(text: str, matches: Matches = None) -> Tuple[list, list, list, list]:
    if matches is None:
        matches = language_check.LanguageTool('en-US').check(text)
    mistakes = []
    corrections = []
    error_start = []
    error_end = []

    for error in matches:
        if len(error.replacements) > 0:
            error_start.append(error.offset)
            error_end.append(error.offset+error.errorlength)
            mistakes.append(text[error_start[-1]:error_end[-1]])
            corrections.append(error.replacements[0])
    return mistakes, corrections, error_start, error_end


def correct_error(text: str, error: Match) -> str:
    corrected_text = list(text)
    for j in range(len(text)):
        if (j > error.offset and j < error.offset + error.errorlength):
            corrected_text[j] = ""

    corrected_text[error.offset] = error.replacements[0]
    return text


def correct_errors(text: str, matches: Matches = None, mistakes=None, corrections=None, start=None, end=None):

    if end is None:
        mistakes, corrections, start, end = manage_errors(text, matches)

    corrected_text = list(text)

    for i in range(len(start)):
        for j in range(len(text)):
            if (j > start[i] and j < end[i]):
                corrected_text[j] = ""

        corrected_text[start[i]] = corrections[i]

    return "".join(corrected_text)
