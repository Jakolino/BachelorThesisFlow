Here is the revised roadmap, updated to reflect a study that does not use MRI and focuses on a purely behavioral test-retest paradigm with 20 participants.

---

### Bachelor Thesis Roadmap

**Adaptive Neuromodulation & Flow-State Reliability: A Behavioral Study**

**1. Literature Review**
- **1.1 Core Topics to Cover**
    - Test–retest reliability in cognitive tasks (focus on behavioral metrics).
    - Flow-state theory (Ulrich et al., 2014; 2022) and its induction.
    - Adaptive task paradigms and cognitive load modeling (e.g., n-back, mental arithmetic).
    - tDCS and tFUS mechanisms, safety, and protocols for single-session application.
    - Cognitive functions of target regions: IFG/mPFC and amygdala.
    - Lifespan considerations in cognition and neuromodulation.

- **1.2 Search Strategy**
    - folder Literatur 
    - Databases: PubMed, Web of Science, Google Scholar, PsyArXiv.
    - Keywords:
        - "test-retest reliability cognitive tasks"
        - "flow state experimental induction"
        - "adaptive n-back" OR "adaptive mental arithmetic"
        - "tDCS cognition" OR "tFUS cognition"
        - "aging executive function neuromodulation"

- **1.3 Deliverables**
    - Annotated bibliography with 15–20 key papers.
    - A written synthesis that identifies the research gap (e.g., reliability of flow-state induction under neuromodulation) and clearly states the project's rationale and hypothesis.

**2. Test Paradigm Development**
- **2.1 Adaptive Mental Arithmetic Task**
    - Implement difficulty adjustment algorithm (e.g., 1-up/1-down staircase) based on accuracy and reaction time.
    - Define and program the recording of key performance metrics: accuracy, reaction time (RT), and intra-individual variability (IIV) as a marker of stability.
    - Program a post-task questionnaire for subjective flow ratings (e.g., Flow Short Scale) and perceived difficulty.

- **2.2 Pilot Testing (Beta Test)**
    - Run 2–3 pilot participants to test the software and workflow.
    - Optimize the difficulty scaling algorithm to prevent floor/celling effects.
    - Refine the timing and instructions based on pilot feedback.

- **2.3 Finalizing the Task Battery**
    - Create two parallel versions of the task (or a method to randomize stimuli) for the two sessions to minimize learning effects.
    - Ensure the task is fully automated and logs all necessary data for later ICC analysis.

**3. Study Materials & Documentation**
- **3.1 Demographic & Screening Questionnaire**
    - Age, Gender, Handedness, Education Level.
    - Neuromodulation-specific contraindications (e.g., metal implants, skin conditions, history of seizures).
    - Current medication and substance use (nicotine, caffeine).

- **3.2 Consent Form**
    - Clear explanation of the study purpose (investigating cognitive performance and flow).
    - Detailed description of the tDCS/tFUS procedure (e.g., sensation, duration).
    - Statement of duration (two sessions), potential risks (e.g., mild tingling, headache), and data confidentiality.
    - Information on compensation (e.g., monetary or course credit).


**4. Recruitment Strategy**
- **4.1 Flyer & Online Text Creation**
    - find draft example in folder flyer
    - contact amelie jung from the Psychologie department for help
    	**E-Mail**: amelie.jung@uni-greifswald.de
	**Telefon**: +49 (0) 3834 420 3776

- **4.3 Scheduling & Tracking**
    - Create a spreadsheet to manage 20 participants.
    - Recruit for two age groups (e.g., 18-30), if applicable.
    - Schedule two sessions per participant, exactly one week apart (or a consistent interval).
    - Counterbalance the order of stimulation conditions (active/sham) across participants.

**5. Statistical Analysis (ICC) Workflow**
- **5.1 Data Collection & Organization**
    - Conduct two sessions per participant (N=20). Administer the adaptive task under either active or sham stimulation in each session.
    - Securely store all behavioral log files.

- **5.2 Data Extraction & Aggregation**
    - Write a script (e.g., in Python or R) to read log files and extract primary outcome variables for each session:
        - Mean Accuracy
        - Mean Reaction Time (for correct trials)
        - Intra-individual Reaction Time Variability (e.g., standard deviation of RT or coefficient of variation)
        - Mean Final Difficulty Level (as a proxy for performance ceiling)
        - Subjective Flow Scale Score

- **5.3 ICC(3,1) Computation**
    - Compile data into a table with one row per participant and separate columns for Session 1 and Session 2 scores for each variable.
    - Use statistical software (e.g., Python's `pingouin.intraclass_corr()` or R's `ICC()` function from the `irr` package) to calculate test-retest reliability.
    - Calculate a separate ICC for each behavioral variable of interest.
    - Use a two-way mixed-effects model for absolute agreement (consistent with test-retest reliability studies).

- **5.4 Interpretation**
    - Interpret ICC values using standard cut-offs:
        - ICC < 0.40 = Poor reliability
        - ICC 0.40–0.75 = Fair to good reliability
        - ICC > 0.75 = Excellent reliability
    - Compare ICCs between the active and sham conditions to assess the effect of neuromodulation on behavioral reliability.

**6. Writing the Thesis**
- **6.1 Structure**
    1.  Introduction
    2.  Theory & Literature Review
    3.  Methods (Participants, Adaptive Task, Neuromodulation Protocol, Procedure)
    4.  Results (Descriptive statistics, ICC reliability tables)
    5.  Discussion (Interpretation of reliability findings, impact of neuromodulation, link to flow theory)
    6.  Limitations & Future Directions (e.g., sample size, lack of neuroimaging)
    7.  References
    8.  Appendices (Questionnaires, task instructions)

- **6.2 Suggested Timeline (6 Months Total)**
    - **Month 1:** Literature review, finalize research question.
    - **Month 2:** Paradigm development, piloting, and ethics submission.
    - **Month 3-4:** Recruitment and data collection (testing 20 participants twice).
    - **Month 5:** Data analysis (ICC computation and interpretation).
    - **Month 6:** Writing, revisions, and final submission.

**7. Final Step**
- Defend thesis (if required).
- Submit final version.
- Celebrate the successful completion of your first major academic milestone and invite me to the party ;)



## Additional Steps

- demographic questionaire in html form
- python script - html to json
- json mit python auswerten

## starting the paradigm

- open a terminal


## Fragebögen

- in word dukument im consent ordner
- BDI von MeMoSLAP kopieren
- Flow-Kurzskala von Rheinberg


- 
