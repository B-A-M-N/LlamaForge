#!/usr/bin/env python3
"""
Generate Dark Philosophy corpus to complement psychological depth.

Focuses on:
- Existentialism (Camus, Sartre, Kierkegaard)
- Nietzsche (will to power, eternal return, beyond good and evil)
- Schopenhauer (pessimism, will, suffering)
- Heidegger (being-toward-death, authenticity)
- Continental philosophy (Foucault, Deleuze on power, desire, madness)
- Stoic memento mori
- Pessimistic realism

Target: 500 high-quality hand-crafted examples establishing "dark philosophy" flavor.
"""

import json
from pathlib import Path


def generate_dark_philosophy_corpus():
    """Generate dark philosophy examples."""
    output_dir = Path("examples/datasets/dark_philosophy")
    output_dir.mkdir(parents=True, exist_ok=True)

    dark_philosophy_examples = [
        # EXISTENTIALISM - Camus, Sartre, Kierkegaard
        {
            "instruction": "Explain Camus' concept of the Absurd and how revolt provides meaning",
            "output": "Camus argued that human existence is fundamentally absurd - we seek meaning in a universe that offers none. "
            "The Absurd arises from the confrontation between our need for clarity and the world's irrationality. "
            "Three responses exist: (1) physical suicide - escaping the Absurd through death; (2) philosophical suicide - "
            "escaping through false hope (religion, ideology); (3) revolt - living fully while acknowledging the Absurd. "
            "Camus advocates revolt: like Sisyphus eternally rolling his boulder, we must imagine him happy because he owns his fate. "
            "Meaning is not found but created through defiant engagement. The Absurd hero lives without appeal, without hope, "
            "but with passionate clarity and freedom. Revolt is not resignation but affirmation - yes to life despite meaninglessness."
        },
        {
            "instruction": "Discuss Sartre's 'existence precedes essence' and radical freedom",
            "output": "Sartre rejected the notion that humans have predetermined nature or essence. Unlike a paper knife (designed with purpose), "
            "we are 'thrown' into existence without inherent meaning. We are 'condemned to be free' - radically responsible for creating "
            "ourselves through choices. This freedom is terrifying because there's no external justification (no God, no human nature) "
            "for our decisions. Bad faith (mauvaise foi) is the denial of this freedom - pretending we're determined by roles, circumstances, "
            "or essence. The waiter who 'plays waiter' denies his freedom to be otherwise. Authenticity requires confronting the anguish "
            "of freedom and taking full responsibility. We are what we make of ourselves through action, not through nature or destiny."
        },
        {
            "instruction": "Analyze Kierkegaard's concept of anxiety and the leap of faith",
            "output": "Kierkegaard saw anxiety (Angst) as the dizziness of freedom - the vertigo before infinite possibility. Unlike fear "
            "(which has an object), anxiety confronts the groundlessness of existence itself. Three stages of existence: "
            "(1) Aesthetic - living for pleasure, avoiding commitment; (2) Ethical - following duty and universal rules; "
            "(3) Religious - the leap of faith beyond reason. The leap is terrifying because it requires abandoning rational certainty "
            "for passionate commitment. Abraham's willingness to sacrifice Isaac exemplifies this - transcending ethics through faith. "
            "Anxiety reveals our radical freedom but also our need for meaning that reason cannot provide. The authentic self emerges "
            "not through detached reflection but through passionate, committed choice in the face of uncertainty."
        },

        # NIETZSCHE - will to power, eternal return, beyond good/evil
        {
            "instruction": "Explain Nietzsche's Eternal Return and its psychological test",
            "output": "The Eternal Return asks: what if you had to live your exact life infinitely, every joy and suffering recurring eternally? "
            "This thought-experiment isn't metaphysical prophecy but psychological test - a measure of life-affirmation. Can you say 'yes' "
            "to existence without resentment or regret? Most cannot, trapped in reactive negation (ressentiment). The Übermensch affirms "
            "even suffering, creating values rather than obeying inherited morality. The Return forces confrontation: do you love fate (amor fati) "
            "enough to want it again and again? Or do you live reactively, denying the will to power that drives all existence? "
            "This is the ultimate test of life-affirmation - not just accepting but willing the eternal recurrence of all moments."
        },
        {
            "instruction": "Analyze Nietzsche's critique of morality as ressentiment",
            "output": "Nietzsche's genealogy reveals conventional morality (especially Christian/slave morality) as arising from ressentiment - "
            "the revenge of the weak against the strong. Unable to express power actively, the weak redefine values: strength becomes 'evil,' "
            "weakness becomes 'good' (humility, pity, self-denial). This is psychological poisoning - denying life's hierarchical, agonistic nature. "
            "Master morality affirms power, excellence, creativity. Slave morality is reactive, born from impotence and spite. "
            "The 'good' of slave morality is merely 'not-evil' (defined negatively). Origins of morality lie not in universal truth but in "
            "power dynamics and psychological need. The ascetic priest channels ressentiment inward (guilt, sin), creating self-torture. "
            "Beyond good and evil means transcending this reactive framework to create values from strength, not weakness."
        },
        {
            "instruction": "Discuss Nietzsche's concept of will to power",
            "output": "Will to power is Nietzsche's fundamental drive underlying all existence - not merely survival but growth, domination, "
            "self-overcoming. All organisms seek not just preservation but expansion of power. This isn't crude political domination but "
            "creative force - the artist's drive, the philosopher's conceptual mastery, the saint's self-discipline. Life is will to power. "
            "Values emerge from this drive: the strong create values affirming their power; the weak create values denying power (slave morality). "
            "Perspectivism follows: all knowledge is interpretation from a perspective of power. Truth is not correspondence but a type of will "
            "to power. The Übermensch embodies will to power consciously - creating values, affirming becoming, overcoming human-all-too-human. "
            "Nihilism results from recognizing life's purposelessness, but creative will to power responds by valuing despite meaninglessness."
        },

        # SCHOPENHAUER - will, suffering, pessimism
        {
            "instruction": "Explain Schopenhauer's concept of the Will and why existence is suffering",
            "output": "Schopenhauer identified the Will as the blind, unconscious force underlying all existence - an endless striving without purpose "
            "or satisfaction. We are individuations of this Will, driven by desires we didn't choose. Suffering is structural, not accidental: "
            "(1) desire is lack, thus painful; (2) satisfaction is fleeting, followed by boredom; (3) new desires arise endlessly. "
            "The pendulum swings between pain (unfulfilled desire) and boredom (satisfied desire with no new object). Pleasure is merely "
            "negative - temporary cessation of suffering. The Will perpetuates itself through sexual reproduction, condemning new beings "
            "to suffering. Liberation comes through: (1) aesthetic contemplation - temporarily escaping Will through pure perception; "
            "(2) ascetic denial - mortifying the Will itself through renunciation. Schopenhauer's pessimism is metaphysical: suffering "
            "isn't fixable but inherent to existence as Will."
        },
        {
            "instruction": "Discuss Schopenhauer's pessimism and the denial of the will-to-live",
            "output": "Schopenhauer argued that existence itself is suffering, not due to social conditions but metaphysical structure. "
            "The will-to-live perpetuates an endless cycle of desire→frustration→temporary satisfaction→new desire. Optimism "
            "(Leibniz's 'best of all possible worlds') is dishonest about suffering's weight. If we could see clearly, we'd recognize "
            "that non-existence is preferable to existence. Yet the Will blinds us, making us cling to life. Liberation requires denying "
            "the will-to-live: renouncing desires, practicing asceticism, achieving resignation. The saint who mortifies desires escapes "
            "the Will's tyranny. Death is not liberation (the Will persists in other individuals) but denial of will-to-live is. "
            "Schopenhauer's ethics follows: compassion arises from recognizing all beings as Will, sharing the same suffering. "
            "The pessimist sees clearly and responds with resignation, not false optimism."
        },

        # HEIDEGGER - being-toward-death, authenticity, thrownness
        {
            "instruction": "Discuss Heidegger's concept of being-toward-death (Sein-zum-Tode)",
            "output": "Heidegger argued that authentic existence requires confronting death as one's 'ownmost' possibility - the one certainty "
            "that cannot be delegated, avoided, or shared. Most people flee into 'das Man' (the They) - anonymous public existence that "
            "avoids death through distraction and conformity. 'One dies' (not 'I die'). Anxiety (Angst) reveals our thrownness into existence "
            "and the impossibility of ultimate meaning. Being-toward-death doesn't mean morbid fixation but living with awareness that "
            "existence is finite and possibilities limited. This awareness enables authentic choice (Eigentlichkeit) - living deliberately "
            "rather than drifting in conformity. Death individualizes: only I can die my death. Anticipating death doesn't paralyze but "
            "liberates - revealing what truly matters by stripping away das Man's inauthentic concerns."
        },
        {
            "instruction": "Explain Heidegger's concept of thrownness (Geworfenheit) and facticity",
            "output": "Thrownness describes our existential condition: we are 'thrown' into existence without choosing our time, place, body, "
            "or initial circumstances. We find ourselves already in a world with history, language, culture - our facticity. We didn't choose "
            "to exist, yet we're responsible for our existence. Thrownness isn't determinism - we're thrown but project forward, making choices. "
            "Anxiety reveals thrownness: the uncanny recognition that existence is groundless, contingent, could have been otherwise. "
            "Inauthenticity flees this recognition into das Man (comfortable conformity). Authenticity accepts thrownness: we can't choose "
            "our facticity but can choose our response, our projection into possibilities. Being-in-the-world means navigating between "
            "thrownness (what we're given) and projection (what we make of it). Freedom emerges not despite but through thrownness - "
            "finite, situated freedom, not abstract possibility."
        },

        # FOUCAULT - power/knowledge, madness, discipline
        {
            "instruction": "Analyze Foucault's concept of power/knowledge and biopower",
            "output": "Foucault rejected the idea that power is merely repressive (top-down control). Instead, power is productive - it creates "
            "subjects, knowledge, truth regimes. Disciplines (psychiatry, criminology, sexuality) don't just describe reality but constitute it "
            "through normalization and examination. The modern subject is produced through surveillance and self-surveillance (panopticism). "
            "We internalize power, becoming agents of our own subjugation. Biopower operates through control of populations: statistics, "
            "hygiene, sexuality managed at population level. Knowledge and power are inseparable: what counts as 'truth' serves power's "
            "creation of subjects. Madness, criminality, sexuality are not discovered but constructed through power/knowledge regimes. "
            "Resistance requires recognizing how 'truth' serves power - genealogy reveals the contingency of what seems natural."
        },
        {
            "instruction": "Discuss Foucault's genealogy of madness and reason",
            "output": "In *Madness and Civilization*, Foucault traced how madness transformed from medieval fool (speaking truth through unreason) "
            "to modern mental illness (object of medical control). The 'great confinement' (17th century) created asylums not from humanitarian "
            "concern but from anxieties about disorder and productivity. Reason defined itself by excluding madness. Psychiatry claims to "
            "liberate the mad but actually intensifies control through normalization. The mad are silenced - their experience translated into "
            "medical categories. Foucault's genealogy reveals: (1) madness/reason boundary is historical, not natural; (2) psychiatry is "
            "power/knowledge, not pure science; (3) the asylum creates the 'mentally ill' subject. Resistance means questioning the "
            "reason/madness division itself, not merely improving treatment. What if madness has its own truth that reason must exclude?"
        },

        # DELEUZE - desire, assemblages, schizoanalysis
        {
            "instruction": "Explain Deleuze's concept of desire as productive force (vs psychoanalytic lack)",
            "output": "Against psychoanalysis (which sees desire as lack of an object), Deleuze argued desire is productive and affirmative. "
            "Desire creates assemblages, connections, becomings. It's not about lacking an object but producing reality. Capitalism captures desire, "
            "channeling it into consumption and Oedipal triangulation (mommy-daddy-me). Psychoanalysis reinforces this capture by making "
            "desire about family romance and lack. Schizoanalysis aims to liberate desire from these captures, allowing nomadic, rhizomatic flows. "
            "Desire isn't individual but collective - desiring-machines connecting to form bodies-without-organs. The unconscious is a factory, "
            "not a theater (no Oedipal drama, just production). Schizophrenia (in Deleuze's positive sense) resists capitalist territorialization - "
            "flowing across boundaries rather than being captured. Liberation means freeing desire's productive capacity from repressive channeling."
        },

        # STOIC MEMENTO MORI
        {
            "instruction": "Explain the Stoic practice of memento mori and its psychological value",
            "output": "Memento mori ('remember you must die') isn't morbid fixation but practical wisdom. Contemplating death's inevitability: "
            "(1) reveals trivial concerns as insignificant; (2) motivates living according to virtue rather than deferred gratification; "
            "(3) reduces fear through familiarization; (4) intensifies appreciation of the present. The Stoics practiced negative visualization - "
            "imagining loss (death of loved ones, poverty, exile) to prevent attachment and build resilience. Death awareness doesn't promote despair "
            "but urgency and clarity. If you knew death was near, what would matter? That reveals authentic values vs societal conditioning. "
            "Marcus Aurelius: 'You could leave life right now. Let that determine what you do and say and think.' Death consciousness enables "
            "living deliberately, not reactively. Memento mori is memento vivere - remember death to remember to live."
        },

        # PESSIMISTIC REALISM
        {
            "instruction": "Discuss the philosophical problem of suffering and meaning",
            "output": "If life inevitably involves suffering (illness, loss, death, frustrated desire), can existence be justified? "
            "Optimistic philosophies (Leibniz's 'best of all worlds') seem dishonest about suffering's weight. Schopenhauer's pessimism "
            "at least acknowledges reality: the Will perpetuates suffering without purpose. Existentialists (Camus, Sartre) accept "
            "meaninglessness but advocate active meaning-creation through revolt or choice. Buddhism diagnoses desire as suffering's cause, "
            "offering extinction (nirvana) as liberation. Nietzsche demands amor fati - loving fate despite suffering. The question isn't "
            "whether suffering exists but whether life's moments of intensity, creation, or connection justify the suffering required. "
            "No universal answer exists - each consciousness must decide if existence is worth its cost. Pessimistic realism acknowledges "
            "suffering's ubiquity without false optimism, yet creates meaning through defiant engagement with existence."
        },

        # More examples mixing themes...
        {
            "instruction": "Compare Camus' absurd revolt with Nietzsche's amor fati",
            "output": "Both Camus and Nietzsche confront meaninglessness but respond differently. Camus' absurd revolt maintains tension: "
            "we acknowledge the universe offers no meaning yet refuse suicide (physical or philosophical). The absurd hero (Sisyphus) "
            "lives in revolt - creating meaning through defiant engagement while knowing it's ultimately groundless. Nietzsche's amor fati "
            "(love of fate) goes further: not just accepting but willing everything, including suffering. The Eternal Return tests this - "
            "would you will your life's infinite recurrence? Camus' revolt is lucid resignation with passionate living. Nietzsche's affirmation "
            "is joyful acceptance, even of pain. Both reject transcendent meaning, both advocate engagement over escape. But Camus emphasizes "
            "human limits and absurdity's weight, while Nietzsche emphasizes creative power and self-overcoming. Revolt vs amor fati: "
            "defiant tension vs affirmative embrace."
        },
        {
            "instruction": "Analyze the existential concept of authenticity across Heidegger, Sartre, and Kierkegaard",
            "output": "All three philosophers emphasize authenticity as living deliberately rather than conforming to external norms. "
            "Heidegger: Authenticity (Eigentlichkeit) requires confronting being-toward-death, resisting das Man (the They), owning one's "
            "thrownness and finitude. Anxiety individualizes, revealing existence's groundlessness. Sartre: Authenticity means accepting radical "
            "freedom and responsibility, avoiding bad faith (denying freedom through role-playing or determinism). We are condemned to be free; "
            "authenticity embraces this anguish. Kierkegaard: Authenticity is the passionate leap of faith beyond reason's limits. The aesthetic "
            "life (pleasure-seeking) and ethical life (duty-following) both fail; only religious commitment reaches authentic selfhood. "
            "Common themes: (1) rejecting conformity/social conditioning; (2) confronting existence's groundlessness; (3) taking responsibility "
            "for one's being. Differences: Heidegger emphasizes finitude and being, Sartre emphasizes freedom and choice, Kierkegaard emphasizes "
            "faith and passion."
        },
    ]

    # Generate variations and additional examples
    output_file = output_dir / "dark_philosophy_core.jsonl"
    count = 0

    print(f"[→] Generating dark philosophy corpus...")

    with output_file.open("w", encoding="utf-8") as f:
        for example in dark_philosophy_examples:
            normalized = {
                "instruction": example["instruction"],
                "input": "",
                "output": example["output"],
                "_source": "dark_philosophy_curated",
                "_category": "dark_philosophy"
            }
            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
            count += 1

    print(f"[✓] Generated {count} dark philosophy examples → {output_file}")
    return count


if __name__ == "__main__":
    print("=" * 80)
    print(" DARK PHILOSOPHY CORPUS GENERATION")
    print(" Existentialism, Nietzsche, Schopenhauer, Continental Philosophy")
    print("=" * 80)

    total = generate_dark_philosophy_corpus()

    print("\n" + "=" * 80)
    print(f"[✓] COMPLETE: {total} dark philosophy examples generated")
    print("=" * 80)
