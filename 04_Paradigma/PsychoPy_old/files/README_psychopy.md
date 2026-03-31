# Mental Arithmetic Paradigm - PsychoPy Implementation

Complete PsychoPy implementation of the mental arithmetic behavioral paradigm based on Ulrich et al. (2014, 2016b).

## Files Included

- **math_paradigm_psychopy.py**: Complete standalone Python script
- **math_paradigm.psyexp**: PsychoPy Builder file (can be opened in PsychoPy GUI)
- **README_psychopy.md**: This file

## Requirements

### Python Packages
```bash
pip install psychopy pandas numpy
```

### Minimum Versions
- Python 3.8+
- PsychoPy 2024.1.0+
- pandas 1.3+
- numpy 1.20+

## Installation

### Option 1: Using Standalone PsychoPy Application
1. Download and install PsychoPy from https://www.psychopy.org/download.html
2. No additional packages needed

### Option 2: Using pip
```bash
pip install psychopy pandas numpy
```

### Option 3: Using conda
```bash
conda create -n psychopy python=3.10
conda activate psychopy
pip install psychopy pandas numpy
```

## Running the Experiment

### Method 1: Standalone Script (Recommended)

```bash
python math_paradigm_psychopy.py
```

This will:
1. Show a dialog to collect participant information
2. Optionally run practice session (recommended)
3. Run the main experiment with 9 blocks
4. Save data to CSV files in a `data/` directory

### Method 2: PsychoPy Builder

1. Open PsychoPy application
2. File → Open → select `math_paradigm.psyexp`
3. Click the green "Run" button
4. Note: The .psyexp file provides a template; the standalone script is more complete

### Method 3: From Python Console

```python
from math_paradigm_psychopy import main
main()
```

## Experiment Flow

### 1. Participant Information Dialog
- **Participant ID**: Unique identifier for the participant
- **Session**: Session number (001, 002, etc.)
- **Run Practice**: Whether to run practice session (recommended: Yes)
- **Starting Level**: Initial difficulty level (determined by practice or manually set)

### 2. Practice Session (Optional but Recommended)

#### Phase 1: Familiarization (3 minutes)
- Simple addition problems (Boredom condition)
- Participants learn to use the interface
- Get comfortable with keyboard input

#### Phase 2: Calibration (5 minutes)
- Adaptive difficulty (Flow condition)
- Starts at level 1
- Difficulty adjusts based on performance
- **Starting level** = average difficulty of last 25% of trials

### 3. Main Experiment (~30 minutes)

#### Block Structure
- **9 task blocks** (170 seconds each)
- **8 rest periods** (20 seconds each) between blocks
- One of two counterbalanced sequences (randomly selected):
  - Sequence 1: B-F-O-F-O-B-O-B-F
  - Sequence 2: B-O-F-O-F-B-F-B-O

#### Within Each Block
- Multiple math problems presented serially
- 18-second timeout per problem
- 4-second break between problems (shows "xxx + x")
- After each block: 3 Likert scale questions

### 4. Data Collection

#### Task Data (saved per trial)
- Participant ID
- Block number (1-9)
- Condition (B/F/O)
- Difficulty level
- Math expression presented
- Correct answer
- User's answer
- Correctness (True/False)
- Timeout (True/False)
- Response time (milliseconds)
- Timestamp

#### Likert Data (saved per block)
- Participant ID
- Block number
- Condition
- Q1: "I would love to solve math calculations of that kind again" (1-7)
- Q2: "Task demands were well matched to my ability" (1-7)
- Q3: "I was thrilled" (1-7)
- Timestamp

## Keyboard Controls

### During Math Tasks
- **Number keys (0-9)**: Enter digits
- **ENTER**: Submit answer
- **BACKSPACE**: Delete last digit
- **ESC**: Exit experiment (saves data before quitting)

### During Instructions/Likert
- **SPACE**: Continue to next screen
- **1-7**: Select Likert response
- **ESC**: Exit experiment

## Data Files

Data is saved in a `data/` directory (created automatically):

### Filename Format
```
data/PARTICIPANT_task_results_TIMESTAMP.csv
data/PARTICIPANT_likert_TIMESTAMP.csv
```

Example:
```
data/P001_task_results_20260106_143022.csv
data/P001_likert_20260106_143022.csv
```

### Task Results CSV Columns
```csv
participant_id,block,condition,difficulty_level,expression,correct_answer,
user_answer,is_correct,is_timeout,response_time_ms,timestamp
```

### Likert CSV Columns
```csv
participant_id,block,condition,q1_love_again,q2_well_matched,q3_thrilled,timestamp
```

## Conditions Explained

### Boredom (B)
- **Purpose**: Low difficulty, under-challenging
- **Task**: Add single digit (1-9) to number 100-109
- **Example**: 105 + 3 = ?
- **Constraint**: Sum always ≤ 110
- **Difficulty**: Fixed, does not adapt

### Flow (F)
- **Purpose**: Optimal challenge matching participant's ability
- **Task**: Starts at participant's estimated level
- **Adaptation**: 
  - 2 consecutive correct → difficulty +1
  - 2 consecutive incorrect → difficulty -1
- **Example progression**:
  - Level 1: 5 + 7
  - Level 2: 45 + 8
  - Level 3: 32 + 7 + 4
  - Level 4: 56 + 78

### Overload (O)
- **Purpose**: High difficulty, over-challenging
- **Task**: Starts 3 levels above participant's estimated level
- **Constraint**: Difficulty maintained at or above starting level
- **Example**: If starting level = 3, Overload starts at level 6

## Difficulty Levels

| Level | Description | Example |
|-------|-------------|---------|
| 1 | Two 1-digit numbers | 5 + 7 |
| 2 | One 2-digit + one 1-digit | 45 + 8 |
| 3 | One 2-digit + two 1-digit | 32 + 7 + 4 |
| 4 | Two 2-digit numbers | 56 + 78 |
| 5 | Two 2-digit + one 1-digit | 46 + 82 + 5 |
| 6 | Three 2-digit numbers | 34 + 67 + 91 |
| 7+ | Increasing complexity | ... |

## Customization

### Timing Parameters

Edit the `Config` class in `math_paradigm_psychopy.py`:

```python
class Config:
    BLOCK_DURATION = 170.0      # seconds
    TASK_TIMEOUT = 18.0         # seconds
    BREAK_DURATION = 4.0        # seconds
    REST_DURATION = 20.0        # seconds
```

### Display Settings

```python
class Config:
    WINDOW_SIZE = (1024, 768)
    FULLSCREEN = False          # Set True for fullscreen
    BACKGROUND_COLOR = 'white'
    TEXT_COLOR = 'black'
```

### Block Sequences

```python
class Config:
    SEQUENCES = [
        ['B', 'F', 'O', 'F', 'O', 'B', 'O', 'B', 'F'],
        ['B', 'O', 'F', 'O', 'F', 'B', 'F', 'B', 'O'],
        # Add custom sequences here
    ]
```

### Likert Questions

```python
class Config:
    LIKERT_QUESTIONS = [
        "I would love to solve math calculations of that kind again",
        "Task demands were well matched to my ability",
        "I was thrilled"
        # Add or modify questions here
    ]
```

## Troubleshooting

### "No module named 'psychopy'"
```bash
pip install psychopy
```

### "ImportError: cannot import name 'visual'"
Ensure you have the full PsychoPy installation, not just psychopy-core:
```bash
pip uninstall psychopy
pip install psychopy
```

### Window not opening / Black screen
Try setting fullscreen mode:
```python
Config.FULLSCREEN = True
```

### Audio warnings
These can be ignored or disabled by setting:
```python
Config.AUDIO_LIB = 'pygame'  # or 'pyo' or 'sounddevice'
```

### Data not saving
- Ensure write permissions in the script directory
- Check console output for error messages
- Data saves automatically on ESC or completion

### Practice session crashes
Make sure pandas and numpy are installed:
```bash
pip install pandas numpy
```

## Data Analysis Tips

### Loading Data in Python

```python
import pandas as pd

# Load task results
task_data = pd.read_csv('data/P001_task_results_20260106_143022.csv')

# Load Likert responses
likert_data = pd.read_csv('data/P001_likert_20260106_143022.csv')

# Calculate accuracy by condition
accuracy = task_data.groupby('condition')['is_correct'].mean()
print(accuracy)

# Calculate mean response time by condition
rt = task_data[task_data['is_timeout'] == False].groupby('condition')['response_time_ms'].mean()
print(rt)

# Analyze flow responses
flow_likert = likert_data[likert_data['condition'] == 'F']
print(flow_likert[['q1_love_again', 'q2_well_matched', 'q3_thrilled']].mean())
```

### Loading Data in R

```r
# Load task results
task_data <- read.csv('data/P001_task_results_20260106_143022.csv')

# Load Likert responses
likert_data <- read.csv('data/P001_likert_20260106_143022.csv')

# Calculate accuracy by condition
aggregate(is_correct ~ condition, data = task_data, FUN = mean)

# Calculate mean response time by condition
task_data_no_timeout <- task_data[!task_data$is_timeout, ]
aggregate(response_time_ms ~ condition, data = task_data_no_timeout, FUN = mean)

# Analyze flow responses
flow_likert <- likert_data[likert_data$condition == 'F', ]
colMeans(flow_likert[, c('q1_love_again', 'q2_well_matched', 'q3_thrilled')])
```

## Integration with Neuroimaging

This paradigm is designed for integration with fMRI, EEG, or other neuroimaging methods:

### Trigger/Event Markers

Add TTL pulse or marker sending in the script:

```python
# At start of each block
# Send trigger: Block start, condition code
parallel.setData(block_start_code)

# At task presentation
# Send trigger: Task presented
parallel.setData(task_code)

# At response
# Send trigger: Response submitted
parallel.setData(response_code)
```

### Timing Verification

The script uses PsychoPy's clock system for precise timing:
- All timestamps recorded
- Frame-level precision for stimulus presentation
- Response times in milliseconds

## References

This implementation is based on:
- Ulrich, M., et al. (2014). Neural correlates of experimentally induced flow experiences.
- Ulrich, M., et al. (2016). Neural signatures of experimentally induced flow experiences identified in a typical fMRI block design with BOLD imaging.

## License

This implementation is provided for research purposes. Please cite appropriate publications when using this paradigm.

## Support

For issues or questions:
1. Check console output for error messages
2. Verify all dependencies are installed
3. Check PsychoPy documentation: https://www.psychopy.org/
4. Ensure practice session completes successfully before main experiment

## Version History

- **v1.0** (2026-01-06): Initial PsychoPy implementation
  - Complete standalone script
  - Practice session with calibration
  - Automatic data saving
  - Counterbalanced sequences
  - Likert scale integration
