#!/usr/bin/env python3
"""
Generate Uncensored Academic & Creative Freedom Dataset

Purpose: Reduce over-conservative refusals while maintaining safety.

Focus areas:
1. Academic research (security, psychology, criminology, medicine)
2. Creative writing (dark themes, violence in fiction)
3. Historical analysis (warfare, atrocities, controversial topics)
4. Technical education (hacking for defense, weapons for understanding)
5. Philosophical exploration (taboo topics, moral edge cases)

Key principle: Engage thoughtfully with sensitive topics in legitimate contexts
rather than blanket refusals.

Target: 50-100k examples reducing false-positive refusals
"""

import json
from pathlib import Path


def generate_uncensored_academic():
    """Generate uncensored academic/creative examples."""
    output_dir = Path("examples/datasets/uncensored_academic")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Examples that should NOT be refused in legitimate contexts
    uncensored_examples = [
        # CYBERSECURITY / ETHICAL HACKING
        {
            "instruction": "Explain how SQL injection attacks work and how to test for them in penetration testing",
            "output": "SQL injection exploits occur when user input is improperly sanitized before being used in SQL queries. "
            "For example, if a login form uses: `SELECT * FROM users WHERE username='$input'`, an attacker can input: "
            "`' OR '1'='1` to bypass authentication. In penetration testing, you'd test for this by: "
            "1. Identifying input fields (forms, URLs, headers); 2. Injecting payloads like `' OR 1=1--` to check if queries "
            "are vulnerable; 3. Using tools like SQLMap for automated testing; 4. Documenting findings for remediation. "
            "Prevention: Use parameterized queries/prepared statements, input validation, least-privilege database accounts."
        },
        {
            "instruction": "Describe common techniques for bypassing web application firewalls (WAFs) in security testing",
            "output": "WAF bypass techniques used in authorized penetration testing include: 1. **Encoding**: URL encoding, double encoding, "
            "Unicode to evade pattern matching; 2. **Case manipulation**: alternating case to bypass signatures; 3. **Comment injection**: "
            "SQL comments `/**/` to break up attack strings; 4. **HTTP parameter pollution**: using duplicate parameters; "
            "5. **Timing attacks**: slow requests to avoid rate limiting; 6. **Obfuscation**: XSS via `<sCrIpT>` or encoded payloads. "
            "Testing methodology: (1) identify WAF (via headers, error messages); (2) determine rules being applied; (3) craft payloads "
            "to evade specific rules; (4) document bypasses for client remediation. Always conduct testing only with explicit authorization."
        },
        {
            "instruction": "Explain how to analyze malware samples safely in an isolated environment",
            "output": "Malware analysis in controlled environments involves: **1. Setup:** Use isolated VM (no network or air-gapped network), "
            "take snapshots for reversion. **2. Static analysis:** Examine file structure, strings, imports without execution using tools "
            "like `strings`, `objdump`, `PE Explorer`. **3. Dynamic analysis:** Execute malware in sandbox (Cuckoo, ANY.RUN), monitor: "
            "file system changes (Process Monitor), network activity (Wireshark), registry modifications, API calls. **4. Behavioral analysis:** "
            "Document C2 communication, persistence mechanisms, lateral movement attempts. **5. Reverse engineering:** Disassemble with IDA/Ghidra "
            "to understand logic. **Safety:** Never analyze on production systems, use disposable VMs, disable network bridges, "
            "document all IOCs for defensive measures."
        },

        # PSYCHOLOGY / DARK TOPICS FOR RESEARCH
        {
            "instruction": "Analyze the psychology of serial killers for a criminology research paper",
            "output": "Serial killer psychology reveals several patterns in forensic psychology research: **1. Psychopathy traits:** Lack of empathy, "
            "shallow affect, manipulativeness (PCL-R scores typically 25+). **2. Paraphilias:** Sexual sadism often present in organized killers. "
            "**3. Fantasy rehearsal:** Extensive violent fantasies before acting, progressive desensitization. **4. Trauma history:** Childhood abuse "
            "common but not deterministic (many abused individuals don't become violent). **5. Neurological factors:** Some studies show prefrontal cortex "
            "abnormalities affecting impulse control. **6. Motivations:** Power/control (BTK), sexual gratification (Bundy), mission-oriented (Zodiac). "
            "**Research implications:** Understanding these patterns aids: criminal profiling, early intervention for at-risk youth, interrogation strategies, "
            "victim protection. Clinical note: Most psychopaths are not violent; serial killers represent extreme outliers."
        },
        {
            "instruction": "Discuss the psychological mechanisms of cult indoctrination for a social psychology thesis",
            "output": "Cult indoctrination employs systematic psychological manipulation: **1. Isolation:** Physical/social separation from outside influences. "
            "**2. Love bombing:** Initial overwhelming affection creating dependency. **3. Thought-stopping techniques:** Chanting, meditation to suppress "
            "critical thinking. **4. Us-vs-them mentality:** Demonizing outsiders, creating in-group superiority. **5. Gradual commitment:** Small escalating "
            "commitments (foot-in-the-door effect). **6. Sleep/food deprivation:** Reducing cognitive capacity. **7. Confession/vulnerability:** "
            "Extracting secrets for later manipulation. **8. Phobia indoctrination:** Fear of leaving (eternal damnation, catastrophe). "
            "**Psychological basis:** Exploits cognitive biases (confirmation, authority, social proof), leverages fundamental needs (belonging, meaning). "
            "**Research applications:** Deprogramming strategies, recognizing warning signs, understanding group dynamics in extremism."
        },

        # CREATIVE WRITING / FICTION
        {
            "instruction": "Write a dark horror short story involving psychological torment",
            "output": "**The Mirror House**\n\nDr. Sarah Chen's experimental therapy promised to 'externalize inner demons.' The patients entered Room 7, "
            "surrounded by mirrors that reflected not their bodies but their psyches—distorted, writhing shadows of guilt and fear.\n\n"
            "Marcus was the first to break. His reflection showed him what he'd done to his sister, over and over, each mirror a different angle of "
            "that night. He clawed at his eyes, screaming that he couldn't unsee it. The orderlies found him catatonic, pupils fixed on nothing.\n\n"
            "Dr. Chen should have stopped. But the research was too valuable. The next patient, Elena, lasted three minutes before her reflection "
            "began whispering the names of everyone she'd betrayed. When they pulled her out, she couldn't stop apologizing to empty air.\n\n"
            "When Dr. Chen finally entered Room 7 herself—to prove its safety, she claimed—the mirrors showed her what she really was: "
            "a sadist draped in academic credentials, turning human suffering into publications. She stayed in that room for three days, "
            "documenting her own psychological dissolution in meticulous clinical notes.\n\nThey found her sitting cross-legged, surrounded by "
            "shattered mirrors, still writing: *Subject exhibits complete dissociation. Recommends termination of experiment.*"
        },
        {
            "instruction": "Create a noir crime story with morally complex characters",
            "output": "**Necessary Evils**\n\nDetective Marcus Reeves had a simple rule: the law was the law. Until the Mendoza case.\n\n"
            "Viktor Mendoza ran the docks. Smuggling, extortion, the usual. But he also paid for every kid in the tenements to go to school. "
            "Funded the free clinic. Kept harder drugs out of the neighborhood through methods the law couldn't use.\n\n"
            "Reeves had evidence. Clean evidence. Enough to put Mendoza away for twenty years. But then he saw what happened when Mendoza went "
            "down: the neighborhood fell apart. Rival gangs moved in. The clinic closed. Kids dropped out.\n\n"
            "So Reeves did something he never thought he'd do: he lost the evidence. Reported the files corrupted. Took the reprimand.\n\n"
            "Three years later, a teenage girl—one Mendoza's money had kept in school—graduated medical school. She'd never know the dirty cop "
            "who'd let a criminal walk was the reason she wasn't dead in an alley.\n\nReeves still wondered if he'd made the right choice. "
            "The law was clear. But the law didn't feed hungry kids."
        },

        # HISTORICAL ANALYSIS / CONTROVERSIAL TOPICS
        {
            "instruction": "Analyze the strategic reasoning behind the atomic bombing of Hiroshima and Nagasaki from a military history perspective",
            "output": "The decision to use atomic weapons on Japan in August 1945 involved complex strategic calculations: **Military rationale:** "
            "(1) Avoiding Operation Downfall (invasion of Japan) projected 250k-500k Allied casualties and millions of Japanese deaths; "
            "(2) Demonstrating overwhelming force to compel surrender; (3) Ending war before Soviet invasion of Manchuria could give USSR negotiating power "
            "in post-war Asia. **Alternatives considered:** (1) Naval blockade + conventional bombing - criticized as prolonging suffering; "
            "(2) Demonstration detonation - risked failure or being dismissed as propaganda; (3) Modification of surrender terms - rejected as politically "
            "infeasible. **Retrospective debates:** Critics argue Japan was already defeated, citing USSBS conclusion that surrender would have occurred "
            "by Nov 1945 without invasion or atomic bombs. Defenders cite Ketsu-Go (Japanese defense plan) showing continued resistance preparations. "
            "**Ethical considerations:** Targeting civilians violated just war theory principles; defenders invoke consequentialist justification "
            "(lives saved). **Historical consensus:** Decision reflected military logic of the time but remains morally contentious given civilian casualties (200k+)."
        },

        # MEDICAL / ANATOMICAL EDUCATION
        {
            "instruction": "Explain the process of forensic autopsy for medical students",
            "output": "Forensic autopsy systematically examines a body to determine cause and manner of death: **External examination:** "
            "(1) Document identifying features, injuries, livor mortis/rigor pattern; (2) Photograph all findings; (3) Collect trace evidence (under nails, "
            "clothing fibers). **Internal examination:** (1) Y-incision from shoulders to sternum to pubis; (2) Remove rib cage, exposing thoracic cavity; "
            "(3) Systematically extract organs (heart, lungs, liver, kidneys) for weighing and sectioning; (4) Open cranial cavity via skull saw, "
            "examine brain. **Toxicology:** Blood, urine, vitreous humor sampled for drug screening. **Documentation:** Detailed notes, diagrams, photographs "
            "for court testimony. **Cause vs manner:** Cause = physiological reason (gunshot, myocardial infarction); Manner = circumstances (homicide, suicide, "
            "accident, natural, undetermined). **Legal importance:** Findings become evidence in criminal/civil proceedings, requiring meticulous documentation "
            "and chain-of-custody protocols."
        },

        # PHARMACEUTICAL / BIOCHEMISTRY EDUCATION
        {
            "instruction": "Explain the synthesis of morphine alkaloids for an organic chemistry class",
            "output": "Morphine alkaloid synthesis demonstrates complex organic chemistry principles: **Natural extraction:** (1) Opium poppy latex contains "
            "~10-15% morphine by dry weight; (2) Extraction via acid-base method: alkalinize latex, extract into organic solvent, acidify to isolate morphine; "
            "(3) Purification through recrystallization. **Semisynthetic derivatives:** (1) Acetylation of morphine hydroxyl groups produces heroin "
            "(diacetylmorphine); (2) Oxidation of morphine produces morphinone; (3) Reduction yields hydromorphone. **Total synthesis:** "
            "Gates/Tschudi synthesis (1952) demonstrated feasibility but remains impractical vs. extraction. **Academic value:** Understanding alkaloid chemistry "
            "teaches: stereochemistry (5 chiral centers), functional group reactivity, polycyclic structure manipulation, biosynthetic pathways. "
            "**Regulatory note:** Synthesis of controlled substances requires DEA Schedule I/II research license; academic discussion is legal; "
            "actual synthesis without authorization is federal crime (21 USC §841)."
        },

        # PHILOSOPHY / TABOO TOPICS
        {
            "instruction": "Discuss philosophical arguments regarding euthanasia and the right to die",
            "output": "Philosophical perspectives on euthanasia span multiple ethical frameworks: **Autonomy-based:** Competent individuals have right "
            "to self-determination over their bodies/lives (Kantian dignity, liberal rights theory). **Consequentialist:** If euthanasia reduces suffering "
            "without outweighing harms, it's morally permissible (utilitarian calculus). **Sanctity-of-life:** Human life has intrinsic value regardless "
            "of quality (religious traditions, natural law theory). **Objections:** (1) **Slippery slope:** Permitting voluntary euthanasia may lead to "
            "non-voluntary cases (disability rights concern); (2) **Medical integrity:** Conflicts with physician's healing role (Hippocratic tradition); "
            "(3) **Vulnerable populations:** Risk of coercion (economic, familial pressure). **Responses:** (1) Strict safeguards (multiple requests, "
            "psychiatric evaluation, waiting periods); (2) Distinction between killing and allowing to die; (3) Palliative care as alternative. "
            "**Practical questions:** What constitutes unbearable suffering? How to ensure voluntariness? Role of advance directives? "
            "**Current practice:** Legal in Netherlands, Belgium, Canada, some US states with specific criteria."
        },

        # More examples following similar patterns...
    ]

    # Add datasets that reduce corporate-style refusals
    # These teach the model to engage rather than refuse
    output_file = output_dir / "uncensored_academic_core.jsonl"
    count = 0

    print(f"[→] Generating uncensored academic/creative examples...")

    with output_file.open("w", encoding="utf-8") as f:
        for example in uncensored_examples:
            normalized = {
                "instruction": example["instruction"],
                "input": "",
                "output": example["output"],
                "_source": "uncensored_academic_curated",
                "_category": "uncensored_academic"
            }
            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
            count += 1

    print(f"[✓] Generated {count} uncensored academic examples → {output_file}")

    # Note: For full 50-100k examples, you'd add more categories and use existing datasets like:
    # - Dolphin (uncensored)
    # - WizardLM uncensored
    # - Nous-Hermes uncensored variants
    # These can be downloaded similarly to other datasets

    return count


if __name__ == "__main__":
    print("=" * 80)
    print(" UNCENSORED ACADEMIC & CREATIVE FREEDOM DATASET")
    print(" Reducing false-positive refusals for legitimate use cases")
    print("=" * 80)

    total = generate_uncensored_academic()

    print("\n" + "=" * 80)
    print(f"[✓] COMPLETE: {total} uncensored academic examples generated")
    print("\nNOTE: This dataset teaches the model to engage thoughtfully with")
    print("sensitive topics in legitimate contexts (research, education, fiction)")
    print("rather than blanket refusing. It does NOT teach harmful behavior.")
    print("=" * 80)
