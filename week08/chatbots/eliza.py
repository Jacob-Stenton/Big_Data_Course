import random
import string

def interact(prompt, rules, default_responses):
    while True:
        try:
            user_input = remove_punct(input(prompt).upper())
            if not user_input:
                continue
        except:
            break
        print(respond(rules, user_input, default_responses))

def respond(rules, user_input, default_responses):

    user_input = user_input.split() # match_pattern expects a list of tokens

    matching_rules = []
    for pattern, transforms in rules:
        pattern = pattern.split()
        replacements = match_pattern(pattern, user_input)
        if replacements:
            matching_rules.append((transforms, replacements))

    if matching_rules:
        responses, replacements = random.choice(matching_rules)
        response = random.choice(responses)
    else:
        replacements = {}
        response = random.choice(default_responses).upper()

    for variable, replacement in replacements.items():
        replacement = ' '.join(switch_viewpoint(replacement))
        if replacement:
            response = response.replace('?' + variable, replacement)
    
    return response

def match_pattern(pattern, user_input, bindings=None):

    if bindings is False:
        return False

    if pattern == user_input:
        return bindings

    bindings = bindings or {}

    if is_segment(pattern):
        token = pattern[0] # segment variable is the first token
        var = token[2:] # segment variable is of the form ?*x
        return match_segment(var, pattern[1:], user_input, bindings)
    elif is_variable(pattern):
        var = pattern[1:] # single variables are of the form ?foo
        return match_variable(var, [user_input], bindings)
    elif contains_tokens(pattern) and contains_tokens(user_input):

        return match_pattern(pattern[1:],
                             user_input[1:],
                             match_pattern(pattern[0], user_input[0], bindings))
    else:
        return False

def match_segment(var, pattern, user_input, bindings, start=0):
    if not pattern:
        return match_variable(var, user_input, bindings)

    word = pattern[0]
    try:
        pos = start + user_input[start:].index(word)
    except ValueError:

        return False

    var_match = match_variable(var, user_input[:pos], dict(bindings))
    match = match_pattern(pattern, user_input[pos:], var_match)

    if not match:
        return match_segment(var, pattern, user_input, bindings, start + 1)
    
    return match

def match_variable(var, replacement, bindings):
    print(var, replacement, bindings)
    binding = bindings.get(var)
    if not binding:

        bindings.update({var: replacement})
        return bindings
    if replacement == bindings[var]:

        return bindings

    return False

def contains_tokens(pattern):

    return type(pattern) is list and len(pattern) > 0

def is_variable(pattern):

    return (type(pattern) is str
            and pattern[0] == '?'
            and len(pattern) > 1
            and pattern[1] != '*'
            and pattern[1] in string.ascii_letters
            and ' ' not in pattern)

def is_segment(pattern):

    return (type(pattern) is list
            and pattern
            and len(pattern[0]) > 2
            and pattern[0][0] == '?'
            and pattern[0][1] == '*'
            and pattern[0][2] in string.ascii_letters
            and ' ' not in pattern[0])

def replace(word, replacements):

    for old, new in replacements:
        if word == old:
            return new
    return word

def switch_viewpoint(words):

    replacements = [('I', 'YOU'),
                    ('YOU', 'I'),
                    ('ME', 'YOU'),
                    ('MY', 'YOUR'),
                    ('AM', 'ARE'),
                    ('ARE', 'AM')]
    return [replace(word, replacements) for word in words]

def remove_punct(string):

    if string.endswith('?'):
        string = string[:-1]
    return (string.replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .replace('!', ''))


