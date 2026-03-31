#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mental Arithmetic Behavioral Paradigm - PsychoPy Implementation (Fixed)
Based on Ulrich et al. (2014, 2016b)

This version implements the correct difficulty scaling:
- Level increase: Replace last 1-digit with 2-digit OR add new 1-digit summand
- Level decrease: Reverse the above steps
"""

import sys
import os
import warnings
warnings.filterwarnings('ignore')

print("Initializing PsychoPy components...")

try:
    from psychopy import visual, core, event, data, gui
    print("✓ PsychoPy imported successfully")
except Exception as e:
    print(f"Error importing PsychoPy: {e}")
    print("\nTroubleshooting steps:")
    print("Check /media/Data03/home/niemannf/psychopy/READM.md")
    sys.exit(1)

import random
import numpy as np
import pandas as pd
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

BLOCK_DURATION = 170.0
TASK_TIMEOUT = 18.0
BREAK_DURATION = 4.0
REST_DURATION = 20.0

CONDITIONS = {'B': 'Boredom', 'F': 'Flow', 'O': 'Overload'}

#SEQUENCES = [
#    ['B','F','O','B','F','B','O','F','O','F','B','O','B','F','O','B','O','F','B','F','O','F','B','O','F','O','B'],
#    ['B','O','F','B','O','B','F','O','F','O','B','F','B','O','F','B','F','O','B','O','F','O','B','F','O','F','B']
#]

SEQUENCES = [
    ['B','F','O','B','F','B','O','F','O','F','B','O'],
    ['B','O','F','B','O','B','F','O','F','O','B','F']
]

# WINDOW_SIZE = (1024, 768)
WINDOW_SIZE = (1400, 1050)
FULLSCREEN = False
BG_COLOR = 'white'
TEXT_COLOR = 'black'

LIKERT_QUESTIONS = [
    "Ich würde solche mathematischen Berechnungen nur zu gern noch einmal lösen",
    #"Die Aufgabenanforderungen entsprachen gut meinen Fähigkeiten", # alte Formulierung
    "Ich fühle mich optimal beansprucht",
    "Ich war begeistert"
]

LIKERT_LABELS = ["Stimme ich \n überhaupt nicht zu", "2", "3", "4", "5", "6", "Stimme ich \n voll zu"]

# ============================================================================
# MATH TASK GENERATOR (FIXED)
# ============================================================================

def create_boredom_task():
    """Boredom: Add single digit (1-9) to 100-109, sum <= 110"""
    base = random.randint(100, 109)
    max_addend = min(9, 110 - base)
    addend = random.randint(1, max_addend)
    numbers = [base, addend]
    return {'text': f'{base} + {addend}', 'answer': sum(numbers), 'numbers': numbers}

def create_flow_task(level):
    """Flow: Task at specified difficulty level"""
    return create_task_at_level(level)

def create_overload_task(level):
    """Overload: Task at specified difficulty level"""
    return create_task_at_level(level)

def create_task_at_level(level):
    """
    Create task at specified difficulty level.
    
    Level structure:
    Level 1: two 1-digit numbers (e.g., 5 + 3)
    Level 2: one 2-digit + one 1-digit (e.g., 45 + 6)
    Level 3: one 2-digit + two 1-digit (e.g., 45 + 6 + 8)
    Level 4: two 2-digit + one 1-digit (e.g., 45 + 67 + 8)
    Level 5: two 2-digit + two 1-digit (e.g., 45 + 67 + 8 + 9)
    Level 6: three 2-digit + one 1-digit (e.g., 45 + 67 + 89 + 5)
    ...and so on
    
    Pattern:
    - Odd levels: last summand is 1-digit
    - Even levels: last summand is 2-digit (or add a new 1-digit at next level)
    """
    if level < 1:
        level = 1
    
    numbers = []
    
    if level == 1:
        # Level 1: two 1-digit numbers
        numbers = [random.randint(1, 9), random.randint(1, 9)]
    else:
        # Calculate number of 2-digit and 1-digit summands
        # Level 2: 1 two-digit, 1 one-digit
        # Level 3: 1 two-digit, 2 one-digit
        # Level 4: 2 two-digit, 1 one-digit
        # Level 5: 2 two-digit, 2 one-digit
        # Level 6: 3 two-digit, 1 one-digit
        # ...
        
        # Number of two-digit numbers = (level - 1) // 2
        # Number of one-digit numbers = ((level - 1) % 2) + 1
        two_digit_count = (level - 1) // 2
        one_digit_count = ((level - 1) % 2) + 1
        
        # Generate two-digit numbers
        for _ in range(two_digit_count):
            numbers.append(random.randint(10, 99))
        
        # Generate one-digit numbers
        for _ in range(one_digit_count):
            numbers.append(random.randint(1, 9))
    
    # Don't shuffle - keep two-digit first, then one-digit for clarity
    # But we can shuffle within each group if desired
    random.shuffle(numbers)
    
    text = ' + '.join(str(n) for n in numbers)
    return {'text': text, 'answer': sum(numbers), 'numbers': numbers}

# ============================================================================
# VISUAL STIMULUS CREATION
# ============================================================================

def create_text_stim(win, text='', pos=(0, 0), height=0.03, bold=False):
    """Helper to create text stimulus"""
    return visual.TextStim(win, text=text, pos=pos, height=height, 
                          color=TEXT_COLOR, bold=bold)

def create_stimuli(win):
    """Create all visual stimuli"""
    stim = {}
    stim['block_info'] = create_text_stim(win, pos=(0, 0.4), height=0.03)
    stim['timer'] = create_text_stim(win, pos=(0, 0.35), height=0.03)
    stim['expression'] = create_text_stim(win, pos=(0, 0.1), height=0.15, bold=True)
    stim['input'] = create_text_stim(win, pos=(0, -0.2), height=0.2)
    stim['input_box'] = visual.Rect(win, width=0.4, height=0.15, pos=(0, -0.2),
                                    lineColor=TEXT_COLOR, lineWidth=2)
    stim['rest'] = create_text_stim(win, text='+', height=0.3, bold=True)
    stim['rest_label'] = create_text_stim(win, text='Rest Period', pos=(0, -0.2))
    stim['instruction'] = create_text_stim(win, height=0.02)
    stim['instruction'].wrapWidth = 1.5
    return stim

# ============================================================================
# DYNAMIC LAYOUT HELPER
# ============================================================================

def compute_expression_layout(expression_text):
    """Return (font_height, expr_y, input_y, box_height) based on expression length.

    The expression font scales down for longer strings so it always fits on one
    line.  The input box is then placed a fixed gap below the expression centre.

    Tuned for WINDOW_SIZE (1400x1050) with units='height'.
    """
    n_chars = len(expression_text)

    # Font height: start big, shrink for longer expressions
    if n_chars <= 9:          # e.g. "5 + 3"
        font_h = 0.15
    elif n_chars <= 14:       # e.g. "45 + 6 + 8"
        font_h = 0.12
    elif n_chars <= 20:       # e.g. "45 + 67 + 8 + 9"
        font_h = 0.09
    elif n_chars <= 28:       # e.g. "45 + 67 + 89 + 5 + 7"
        font_h = 0.07
    else:
        font_h = 0.055

    # Expression sits in the upper half; input box sits below with a fixed gap
    expr_y   =  0.15
    gap      =  font_h * 0.8 + 0.12   # half-line + breathing room
    input_y  =  expr_y - gap
    box_h    =  font_h * 1.1          # box scales with font

    return font_h, expr_y, input_y, box_h


def update_layout_for_expression(stim, expression_text):
    """Resize and reposition expression + input box to fit expression_text."""
    font_h, expr_y, input_y, box_h = compute_expression_layout(expression_text)

    stim['expression'].pos    = (0, expr_y)
    stim['expression'].height = font_h

    stim['input'].pos         = (0, input_y)
    stim['input'].height      = font_h * 0.9   # answer slightly smaller

    stim['input_box'].pos     = (0, input_y)
    stim['input_box'].height  = box_h


# ============================================================================
# LIKERT SCALE
# ============================================================================

def create_likert_elements(win, question):
    """Create Likert scale visual elements"""
    elements = {}
    
    elements['question'] = visual.TextStim(
        win, text=question, pos=(0, 0.35), height=0.03,
        color=TEXT_COLOR, wrapWidth=1.4, bold=True
    )
    
    scale_positions = np.linspace(-0.6, 0.6, 7)
    elements['circles'] = []
    elements['labels'] = []
    
    for i, x_pos in enumerate(scale_positions):
        circle = visual.Circle(win, radius=0.03, pos=(x_pos, 0),
                              lineColor=TEXT_COLOR, lineWidth=2, fillColor=None)
        elements['circles'].append(circle)
        
        label = visual.TextStim(win, text=LIKERT_LABELS[i], pos=(x_pos, -0.15),
                               height=0.015, color=TEXT_COLOR, alignText='center')
        elements['labels'].append(label)
    
    elements['instruction'] = visual.TextStim(
        win, text="Press 1-7 to select your response",
        pos=(0, -0.35), height=0.02, color=TEXT_COLOR
    )
    
    return elements

def get_likert_response(win, question):
    """Get response to a single Likert scale question"""
    elements = create_likert_elements(win, question)
    selected = None
    
    while selected is None:
        elements['question'].draw()
        elements['instruction'].draw()
        for circle, label in zip(elements['circles'], elements['labels']):
            circle.draw()
            label.draw()
        win.flip()
        
        keys = event.waitKeys(keyList=['1','2','3','4','5','6','7','escape',
                                       'num_1','num_2','num_3','num_4','num_5','num_6','num_7'])
        
        if 'escape' in keys:
            raise KeyboardInterrupt
        
        key = keys[0]
        if key.startswith('num_'):
            selected = int(key.split('_')[1])
        else:
            selected = int(key)
    
    # Show selection
    elements['circles'][selected - 1].fillColor = TEXT_COLOR
    elements['question'].draw()
    for circle, label in zip(elements['circles'], elements['labels']):
        circle.draw()
        label.draw()
    win.flip()
    core.wait(0.5)
    
    return selected

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def show_instructions(win, stim, text):
    """Show instruction screen"""
    stim['instruction'].text = text
    stim['instruction'].draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])

def show_rest(win, stim):
    """Show rest period"""
    print("Rest period...")
    stim['rest'].draw()
    stim['rest_label'].draw()
    win.flip()
    core.wait(REST_DURATION)

def make_placeholder(numbers):
    """Build a placeholder string matching the digit-count structure of numbers.

    Each number is replaced by as many 'x' characters as it has digits,
    preserving the ' + ' separators so the participant can see the shape
    of the upcoming calculation (e.g. [40, 23, 5] -> 'xx + xx + x').
    """
    return ' + '.join('x' * len(str(n)) for n in numbers)


def show_break(win, stim, next_numbers=None):
    """Show inter-trial break.

    If next_numbers is provided the placeholder mirrors the digit structure
    of the upcoming expression (e.g. [40, 23, 5] -> 'xx + xx + x').
    Falls back to 'xxx + x' when next_numbers is None.
    """
    placeholder = make_placeholder(next_numbers) if next_numbers else 'xxx + x'
    stim['expression'].text = placeholder
    update_layout_for_expression(stim, placeholder)
    stim['input'].text = ''
    stim['timer'].text = 'Break'
    stim['block_info'].draw()
    stim['timer'].draw()
    stim['expression'].draw()
    win.flip()
    core.wait(BREAK_DURATION)

# ============================================================================
# TRIAL EXECUTION (FIXED DIFFICULTY UPDATE)
# ============================================================================

def update_difficulty(is_correct, current_level, consecutive_correct, consecutive_incorrect, 
                     condition, starting_level):
    """
    Update difficulty for Flow/Overload conditions.
    
    Rules:
    - Two correct answers in a row: increase level by 1
    - Two incorrect answers in a row: decrease level by 1
    - Overload condition: maintain level >= starting_level
    """
    if is_correct:
        consecutive_correct += 1
        consecutive_incorrect = 0
        if consecutive_correct >= 2:
            current_level += 1
            consecutive_correct = 0
            print(f"  ✓✓ Two correct! Difficulty increased to level {current_level}")
    else:
        consecutive_incorrect += 1
        consecutive_correct = 0
        if consecutive_incorrect >= 2:
            new_level = current_level - 1
            
            # For overload condition, maintain minimum level
            if condition == 'O':
                new_level = max(starting_level, new_level)
            else:
                new_level = max(1, new_level)
            
            if new_level != current_level:
                print(f"  ✗✗ Two incorrect! Difficulty decreased to level {new_level}")
            else:
                print(f"  ✗✗ Two incorrect! Difficulty stays at minimum level {current_level}")
            
            current_level = new_level
            consecutive_incorrect = 0
    
    return current_level, consecutive_correct, consecutive_incorrect

def collect_keyboard_input(win, stim, clock, block_clock, expression):
    """Collect keyboard input for a trial"""
    user_input = ''
    stim['input'].text = ''
    submitted = False
    timeout = False
    
    while not submitted and clock.getTime() < TASK_TIMEOUT:
        if block_clock.getTime() >= BLOCK_DURATION:
            timeout = True
            break
        
        remaining = int(TASK_TIMEOUT - clock.getTime())
        stim['timer'].text = f"Time: {remaining}s"
        
        stim['block_info'].draw()
        stim['timer'].draw()
        stim['expression'].draw()
        stim['input_box'].draw()
        stim['input'].draw()
        win.flip()
        
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                raise KeyboardInterrupt
            elif key == 'return':
                submitted = True
                break
            elif key == 'backspace':
                user_input = user_input[:-1]
                stim['input'].text = user_input
            elif key in '0123456789':
                user_input += key
                stim['input'].text = user_input
            elif key.startswith('num_'):
                user_input += key.split('_')[1]
                stim['input'].text = user_input
    
    if not submitted:
        timeout = True
    
    response_time = clock.getTime() * 1000
    
    if timeout or user_input == '':
        user_answer = None
        is_correct = False
    else:
        try:
            user_answer = int(user_input)
            is_correct = (user_answer == expression['answer'])
        except ValueError:
            user_answer = None
            is_correct = False
    
    return user_answer, is_correct, timeout, response_time

def run_trial(win, stim, condition, level, block_idx, block_clock, participant_id, 
              task_results, starting_level):
    """Run a single trial"""
    if block_clock.getTime() >= BLOCK_DURATION:
        return level, 0, 0
    
    # Use pre-generated task from break screen if available, otherwise generate fresh
    if '_prefetched_task' in stim and stim['_prefetched_task'] is not None:
        expression = stim['_prefetched_task']
        stim['_prefetched_task'] = None
    else:
        if condition == 'B':
            expression = create_boredom_task()
        elif condition == 'F':
            expression = create_flow_task(level)
        else:  # 'O'
            expression = create_overload_task(level)
    
    stim['expression'].text = expression['text']
    update_layout_for_expression(stim, expression['text'])

    # Collect response
    clock = core.Clock()
    user_answer, is_correct, timeout, response_time = collect_keyboard_input(
        win, stim, clock, block_clock, expression
    )
    
    # Store result
    task_results.append({
        'participant_id': participant_id,
        'block': block_idx + 1,
        'condition': condition,
        'difficulty_level': level,
        'expression': expression['text'],
        'correct_answer': expression['answer'],
        'user_answer': user_answer,
        'is_correct': is_correct,
        'is_timeout': timeout,
        'response_time_ms': response_time,
        'timestamp': datetime.now().isoformat()
    })
    
    return is_correct

# ============================================================================
# BLOCK EXECUTION
# ============================================================================

def run_block(win, stim, condition, starting_level, block_idx, participant_id, task_results):
    """Run a single block of trials"""
    if condition == 'B':
        level = 1
        block_starting_level = 1
    elif condition == 'F':
        level = starting_level
        block_starting_level = starting_level
    else:  # 'O'
        level = starting_level + 3
        block_starting_level = starting_level + 3
    
    consecutive_correct = 0
    consecutive_incorrect = 0
    
    condition_name = CONDITIONS[condition]
    stim['block_info'].text = f"Block {block_idx + 1}/12 - Condition: {condition_name}"
    
    print(f"\nStarting Block {block_idx + 1} - {condition_name} (Level {level})")
    
    block_clock = core.Clock()
    trial_count = 0
    
    while block_clock.getTime() < BLOCK_DURATION:
        trial_count += 1
        is_correct = run_trial(win, stim, condition, level, block_idx,
                              block_clock, participant_id, task_results, block_starting_level)

        if condition in ['F', 'O']:
            level, consecutive_correct, consecutive_incorrect = update_difficulty(
                is_correct, level, consecutive_correct, consecutive_incorrect,
                condition, block_starting_level
            )

        # Pre-generate the next task so the break placeholder mirrors its structure
        if block_clock.getTime() < BLOCK_DURATION:
            if condition == 'B':
                next_task = create_boredom_task()
            elif condition == 'F':
                next_task = create_flow_task(level)
            else:
                next_task = create_overload_task(level)
            show_break(win, stim, next_numbers=next_task['numbers'])
            # Cache it so run_trial can use it on the next iteration
            stim['_prefetched_task'] = next_task
        else:
            show_break(win, stim)

    print(f"Block {block_idx + 1} complete: {trial_count} trials, final level: {level}")

def run_likert(win, condition, block_idx, participant_id, likert_responses):
    """Run Likert questionnaire"""
    print("Likert questionnaire...")
    responses = []
    
    for question in LIKERT_QUESTIONS:
        response = get_likert_response(win, question)
        responses.append(response)
    
    likert_responses.append({
        'participant_id': participant_id,
        'block': block_idx + 1,
        'condition': condition,
        'q1_love_again': responses[0],
        'q2_well_matched': responses[1],
        'q3_thrilled': responses[2],
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# DATA SAVING
# ============================================================================

def save_data(participant_id, task_results, likert_responses):
    """Save all collected data to files"""
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if task_results:
        task_df = pd.DataFrame(task_results)
        task_filename = f"{data_dir}/{participant_id}_task_results_{timestamp}.csv"
        task_df.to_csv(task_filename, index=False)
        print(f"✓ Task results saved to: {task_filename}")
    
    if likert_responses:
        likert_df = pd.DataFrame(likert_responses)
        likert_filename = f"{data_dir}/{participant_id}_likert_{timestamp}.csv"
        likert_df.to_csv(likert_filename, index=False)
        print(f"✓ Likert responses saved to: {likert_filename}")

# ============================================================================
# PRACTICE SESSION
# ============================================================================

def run_practice_trial(win, stim_dict, task_generator_func, clock, level=None):
    """Run a single practice trial"""
    # Use pre-generated task from the previous break screen if available
    if '_prefetched_task' in stim_dict and stim_dict['_prefetched_task'] is not None:
        expression = stim_dict['_prefetched_task']
        stim_dict['_prefetched_task'] = None
    elif level is None:
        expression = task_generator_func()
    else:
        expression = task_generator_func(level)
    
    stim_dict['expression'].text = expression['text']
    update_layout_for_expression(stim_dict, expression['text'])
    user_input = ''
    stim_dict['input'].text = ''
    submitted = False
    
    task_clock = core.Clock()
    
    while not submitted and task_clock.getTime() < TASK_TIMEOUT:
        remaining = int(TASK_TIMEOUT - task_clock.getTime())
        stim_dict['timer'].text = f"Time: {remaining}s"
        
        stim_dict['timer'].draw()
        stim_dict['expression'].draw()
        stim_dict['input_box'].draw()
        stim_dict['input'].draw()
        win.flip()
        
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                return None, False
            elif key == 'return':
                submitted = True
                break
            elif key == 'backspace':
                user_input = user_input[:-1]
                stim_dict['input'].text = user_input
            elif key in '0123456789' or key.startswith('num_'):
                if key.startswith('num_'):
                    user_input += key.split('_')[1]
                else:
                    user_input += key
                stim_dict['input'].text = user_input
    
    is_correct = False
    if user_input:
        try:
            user_answer = int(user_input)
            is_correct = (user_answer == expression['answer'])
        except ValueError:
            pass
    
    return expression, is_correct

def run_practice_block(win, condition_type, duration_sec, start_level=1):
    """Run a practice block. start_level sets the initial difficulty for the flow calibration."""
    stim_dict = {}
    stim_dict['expression'] = create_text_stim(win, pos=(0, 0.1), height=0.15, bold=True)
    stim_dict['input'] = create_text_stim(win, pos=(0, -0.1), height=0.1)
    stim_dict['input_box'] = visual.Rect(win, width=0.4, height=0.15, pos=(0, -0.1),
                                         lineColor=TEXT_COLOR, lineWidth=2)
    stim_dict['timer'] = create_text_stim(win, pos=(0, 0.35), height=0.05)
    
    clock = core.Clock()
    levels = []
    current_level = max(1, start_level)
    consecutive_correct = 0
    consecutive_incorrect = 0
    
    while clock.getTime() < duration_sec:
        if condition_type == 'boredom':
            expression, is_correct = run_practice_trial(win, stim_dict, create_boredom_task, clock)
        else:  # flow
            expression, is_correct = run_practice_trial(win, stim_dict, create_flow_task, clock, current_level)
            levels.append(current_level)

            if expression and is_correct is not None:
                if is_correct:
                    consecutive_correct += 1
                    consecutive_incorrect = 0
                    if consecutive_correct >= 2:
                        current_level += 1
                        consecutive_correct = 0
                else:
                    consecutive_incorrect += 1
                    consecutive_correct = 0
                    if consecutive_incorrect >= 2:
                        current_level = max(1, current_level - 1)
                        consecutive_incorrect = 0

        if expression is None:  # ESC pressed
            return []

        # Show placeholder for the NEXT task (pre-generate to get its structure)
        if clock.getTime() < duration_sec:
            if condition_type == 'boredom':
                next_task = create_boredom_task()
            else:
                next_task = create_flow_task(current_level)
            placeholder = make_placeholder(next_task['numbers'])
            stim_dict['_prefetched_task'] = next_task
        else:
            placeholder = 'xxx + x'
            stim_dict['_prefetched_task'] = None

        stim_dict['expression'].text = placeholder
        update_layout_for_expression(stim_dict, placeholder)
        stim_dict['input'].text = ''
        stim_dict['expression'].draw()
        win.flip()
        core.wait(2.0)

    return levels

def run_practice_session():
    """Run practice session to estimate starting level"""
    exp_info = {'Participant ID': '', 'Session': '001'}
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Practice Session',
                         order=['Participant ID', 'Session'])
    
    if not dlg.OK:
        core.quit()
    
    participant_id = exp_info['Participant ID']
    print("Creating practice window...")
    
    win = visual.Window(size=WINDOW_SIZE, fullscr=FULLSCREEN, color=BG_COLOR,
                       units='height', allowGUI=True)
    
    instruction = create_text_stim(win, height=0.02)
    instruction.wrapWidth = 1.4
    instruction.text = (
        "Practice Session\n\n"
        "First, you'll practice with simple problems (3 min).\n"
        "Then, we'll estimate your skill level (5 min).\n\n"
        "Press SPACE to begin."
    )
    instruction.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    print("Running familiarization phase...")
    run_practice_block(win, 'boredom', 180)
    
    print("Running calibration phase...")
    levels = run_practice_block(win, 'flow', 300)
    
    if levels:
        last_quarter = levels[-len(levels)//4:]
        starting_level = max(1, int(np.mean(last_quarter)))
    else:
        starting_level = 1
    
    print(f"Estimated starting level: {starting_level}")
    
    result = create_text_stim(win, height=0.02)
    result.wrapWidth = 1.4
    result.text = (
        f"Practice Complete!\n\n"
        f"Your estimated starting level: {starting_level}\n\n"
        f"Press SPACE to continue to main experiment."
    )
    result.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    win.close()
    return participant_id, starting_level

# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_main_experiment(participant_id, starting_level):
    """Run the main experiment"""
    sequence = random.choice(SEQUENCES)
    print(f"Selected sequence: {'-'.join(sequence)}")
    
    win = visual.Window(size=WINDOW_SIZE, fullscr=FULLSCREEN, color=BG_COLOR,
                       units='height', allowGUI=True)
    
    stim = create_stimuli(win)
    task_results = []
    likert_responses = []
    
    try:
        show_instructions(win, stim, 
            "Welcome to the Mental Arithmetic Task\n\n"
            "You will solve addition problems.\n"
            "Type your answer using the keyboard.\n"
            "Press ENTER to submit.\n\n"
            "Press SPACE to begin."
        )
        
        for block_idx in range(len(sequence)):
            if block_idx > 0:
                show_rest(win, stim)
            
            condition = sequence[block_idx]
            run_block(win, stim, condition, starting_level, block_idx,
                     participant_id, task_results)
            run_likert(win, condition, block_idx, participant_id, likert_responses)
        
        show_instructions(win, stim,
            "Experiment Complete!\n\n"
            "Thank you for participating.\n\n"
            "Press SPACE to save and exit."
        )
        
        save_data(participant_id, task_results, likert_responses)
        
    except KeyboardInterrupt:
        print("\nExperiment interrupted")
        save_data(participant_id, task_results, likert_responses)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        save_data(participant_id, task_results, likert_responses)
    finally:
        win.close()
        core.quit()

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point.

    The startup dialog offers three independent checkboxes so that each phase
    can be run on its own or combined in any combination:

      Run Familiarization   – 3-min boredom-level warm-up block
      Run Skill Evaluation  – 5-min adaptive calibration to estimate starting level
      Run Main Experiment   – the full 12-block paradigm

    If Skill Evaluation is unchecked the manually entered Starting Level is used.
    If only Familiarization is checked the script ends after the warm-up.
    """
    print("\n" + "="*60)
    print("Mental Arithmetic Behavioral Paradigm")
    print("="*60 + "\n")

    exp_info = {
        'Participant ID': '',
        'Session': '001',
        'Run Familiarization': True,
        'Run Skill Evaluation': True,
        'Run Main Experiment': True,
        'Starting Level (if no Skill Eval)': 1,
    }

    dlg = gui.DlgFromDict(
        dictionary=exp_info,
        title='Mental Arithmetic Paradigm',
        order=[
            'Participant ID',
            'Session',
            'Run Familiarization',
            'Run Skill Evaluation',
            'Run Main Experiment',
            'Starting Level (if no Skill Eval)',
        ]
    )

    if not dlg.OK:
        print("Experiment cancelled")
        core.quit()

    participant_id        = exp_info['Participant ID']
    run_familiarization   = exp_info['Run Familiarization']
    run_skill_eval        = exp_info['Run Skill Evaluation']
    run_main              = exp_info['Run Main Experiment']
    starting_level        = int(exp_info['Starting Level (if no Skill Eval)'])

    # ── Familiarization only (warm-up, no calibration) ───────────────────────
    if run_familiarization and not run_skill_eval:
        print("\n=== Starting Familiarization (warm-up only) ===\n")
        win = visual.Window(size=WINDOW_SIZE, fullscr=FULLSCREEN, color=BG_COLOR,
                            units='height', allowGUI=True)
        instruction = create_text_stim(win, height=0.02)
        instruction.wrapWidth = 1.4
        instruction.text = (
            "Familiarization\n\n"
            "You will practice with simple problems for 3 minutes.\n\n"
            "Press SPACE to begin."
        )
        instruction.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        run_practice_block(win, 'boredom', 180)
        done = create_text_stim(win, height=0.02)
        done.wrapWidth = 1.4
        done.text = "Familiarization complete.\n\nPress SPACE to exit."
        done.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        win.close()
        print("=== Familiarization complete ===")
        if not run_main:
            core.quit()

    # ── Skill Evaluation (with optional familiarization prefix) ──────────────
    if run_skill_eval:
        print("\n=== Starting Practice Session ===\n")
        win = visual.Window(size=WINDOW_SIZE, fullscr=FULLSCREEN, color=BG_COLOR,
                            units='height', allowGUI=True)
        instruction = create_text_stim(win, height=0.02)
        instruction.wrapWidth = 1.4

        if run_familiarization:
            instruction.text = (
                "Practice Session\n\n"
                "First, you'll practice with simple problems (3 min).\n"
                "Then, we'll estimate your skill level (5 min).\n\n"
                "Press SPACE to begin."
            )
            instruction.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            print("Running familiarization phase...")
            run_practice_block(win, 'boredom', 180)
        else:
            instruction.text = (
                "Skill Evaluation\n\n"
                "We will now estimate your starting level (5 min).\n\n"
                "Press SPACE to begin."
            )
            instruction.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

        print("Running skill evaluation phase...")
        levels = run_practice_block(win, 'flow', 300, start_level=starting_level)

        if levels:
            last_quarter = levels[-max(1, len(levels) // 4):]
            starting_level = max(1, int(np.mean(last_quarter)))
        else:
            starting_level = 1

        print(f"Estimated starting level: {starting_level}")

        result = create_text_stim(win, height=0.02)
        result.wrapWidth = 1.4
        if run_main:
            result.text = (
                f"Practice Complete!\n\n"
                f"Your estimated starting level: {starting_level}\n\n"
                f"Press SPACE to continue to the main experiment."
            )
        else:
            result.text = (
                f"Skill Evaluation Complete!\n\n"
                f"Estimated starting level: {starting_level}\n\n"
                f"Press SPACE to exit."
            )
        result.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        win.close()

        if not run_main:
            print(f"=== Skill Evaluation complete — starting level: {starting_level} ===")
            core.quit()

    # ── Main Experiment ───────────────────────────────────────────────────────
    if run_main:
        print(f"\n=== Starting Main Experiment ===")
        print(f"Participant: {participant_id}")
        print(f"Starting level: {starting_level}\n")
        run_main_experiment(participant_id, starting_level)
        print("\n=== Experiment Complete ===\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
