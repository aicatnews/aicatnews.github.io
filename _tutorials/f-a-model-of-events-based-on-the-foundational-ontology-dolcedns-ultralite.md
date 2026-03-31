---
layout: default
title: "F -- A Model of Events based on the Foundational Ontology DOLCE+DnS Ultralite"
---


- **ArXiv URL**: http://arxiv.org/abs/2411.16609v1

- **Author**: Steffen Staab; C. Saathoff; Thomas Franz; A. Scherp

- **Publisher**: University of Koblenz-Landau

---

## TL;DR
This paper proposes an event formalization model called Event-Model-F (F), which is based on the foundational ontology DOLCE+DnS Ultralite (DUL). Using a pattern-driven approach, it comprehensively represents time, space, participating entities, structural relations (part-whole, causal, correlative), and different subjective interpretations of the same event, in order to address poor interoperability in distributed event systems.

## Key Definitions
*   **Event-Model-F (F)**: An event formalization model proposed in this paper for capturing and representing human experience. It does not focus on technical events inside computer systems, but on real-world events involving human participation that can be discussed and interpreted.
*   **Foundational Ontology (DOLCE+DnS Ultralite)**: The upper-level foundational ontology on which the F model is based. DOLCE provides distinctions among basic categories such as Event, Object, Quality, and Abstract. The F model follows its design principles, especially by leveraging its Descriptions and Situations (DnS) pattern.
*   **Ontology Patterns**: The core design method of the F model. It breaks down complex event descriptions into a series of independent, reusable pattern modules, each responsible for describing one specific aspect of an event.
*   **Descriptions and Situations (DnS)**: A core pattern in DUL that the F model extensively adopts to formally represent different contextualized views of events. This pattern separates events (occurrences in the real world) from their descriptions (subjective, interpretable views), making it possible to model different interpretations of the same event.
*   **Mereology**: A philosophical concept describing compositional relations between events. In the F model, it refers to structural relations in which an event can be composed of other sub-events.

## Related Work
At present, the number of systems that handle events, such as media distribution and emergency response systems, is growing rapidly, but these systems usually use different internal data models, resulting in poor interoperability. Existing event models, such as Eventory, CIDOC CRM, and EventML, are mostly designed for specific domains, lack a systematic development methodology, are conceptually narrow, and are semantically ambiguous.

The main bottlenecks of these models are:
1.  **Insufficient support for structural relations**: Their ability to model part-whole (mereological), causal, and correlative relations between events is very limited or completely absent.
2.  **Lack of subjectivity modeling**: They cannot represent different subjective interpretations or viewpoints of the same event from different observers.
3.  **Low degree of formalization**: They lack strict formalization and axiomatization, making it difficult for machines to perform automatic semantic validation and reasoning, which hinders interoperability between systems.

This paper aims to solve the above problems by creating a general event model that is formal, extensible, modular, and reusable, so as to support precise representation of complex events, especially their structural relations and multiple interpretations.

## Method
The design of Event-Model-F (F) strictly follows the foundational ontology DOLCE+DnS Ultralite (DUL) and its pattern-driven design philosophy. Its core innovation lies in using DUL’s Descriptions and Situations (DnS) pattern to break down complex event descriptions into six independent, composable ontology patterns.

<img src="/images/2411.16609v1/MotivationSlide.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

### Innovation
Unlike previous models that directly describe event attributes, the core mechanism of the F model is to **separate the description of an event (Description) from the situation in which the event itself occurs (Situation)**. This allows the model to distinguish between “what happened in the world” (Situation) and “how we view and describe it” (Description). This design makes it possible for multiple, even contradictory, interpretations of the same event to coexist and be formally modeled.

### Model Architecture: Six Ontology Patterns
The F model consists of the following six DnS-based patterns, which together enable a comprehensive description of events.

<img src="/images/2411.16609v1/x1.jpg" alt="Figure illustration" style="width:85%; max-width:450px; margin:auto; display:block;">

1.  **Participation Pattern**:
    *   **Function**: Describes how objects (people, things) participate in an event and play specific roles.
    *   **Implementation**: It links an event ($$DUL:Event$$) and participating objects ($$DUL:Object$$) through $$F:EventParticipationSituation$$. $$F:EventParticipationDescription$$ is used to define the specific event type ($$F:DescribedEvent$$) and participant roles ($$F:Participant$$). At the same time, it can also define the absolute time at which the event occurs and the absolute space in which the object exists.

2.  **Mereology Pattern**:
    *   **Function**: Expresses compositional relations between events, that is, a complex “composite event” is made up of multiple “component events.”
    *   **Implementation**: $$F:EventCompositionSituation$$ contains a composite event (classified as $$F:Composite$$) and multiple component events (classified as $$F:Component$$). This pattern also allows spatiotemporal constraints to be imposed on component events, thereby supporting the modeling of relative temporal and spatial relations.

3.  **Causality Pattern**:
    *   **Function**: Formally represents causal chains between events, that is, one event (the cause) leads to another event (the effect).
    *   **Implementation**: It defines two event types, $$F:Cause$$ and $$F:Effect$$. The key point is that it also introduces the concept of $$F:Justification$$, used to explain the theory or belief on which the causal relation is based (such as physical laws or personal opinions), making the determination of causality explicit and traceable.

4.  **Correlation Pattern**:
    *   **Function**: Describes correlations between two or more events, meaning they may be caused by a common but unknown “common cause,” without a direct causal relation between them.
    *   **Implementation**: It defines the $$F:Correlate$$ role to classify correlated events, and likewise uses $$F:Justification$$ to explain the theory or rule behind the correlation. This is very useful when causality is difficult to determine.

5.  **Documentation Pattern**:
    *   **Function**: Provides evidential support for the occurrence of an event.
    *   **Implementation**: It defines $$F:DocumentedEvent$$ (the documented event) and $$F:Documenter$$ (the document provider). $$Documenter$$ can be any $$DUL:Object$$ (such as photos or sensor data) or $$DUL:Event$$, providing a basis for the event’s authenticity.

6.  **Interpretation Pattern**:
    *   **Function**: This is the core glue of the entire model, used to integrate all the above patterns into a specific, self-consistent “interpretation” or “viewpoint” of an event.
    *   **Implementation**: It defines $$F:Interpretant$$ to classify the interpreted event. An interpretation consists of a series of relevant situations ($$F:RelevantSituations$$), which are concrete instances of the participation, composition, causality, correlation, and documentation patterns. By creating multiple different interpretation instances, different or even conflicting viewpoints of the same event (such as a “power outage”) can be formed, for example “a utility pole was blown down by the wind” vs. “the power plant malfunctioned.”

### Advantages
*   **Formalization and axiomatization**: Based on DUL, it has rigorous semantics and supports machine reasoning and validity verification.
*   **Modularity and reusability**: The pattern-based design allows users to select and combine different modules as needed, simplifying development and application.
*   **Scalability**: It can be easily extended by defining new patterns or combining it with domain ontologies.
*   **Separation of concerns**: It clearly separates the structural knowledge of events (defined by F) from domain-specific knowledge (defined by the domain ontology).

## Experimental Conclusions

This paper did not conduct traditional quantitative experiments, but instead validated its advantages through an application example in an emergency response scenario and a comparative analysis with existing models.

### Validation Through an Application Example
In an emergency response scenario, the F model can clearly describe complex events. For example, for a “power outage” event:
*   **The causal pattern** can represent that “a utility pole breaking” caused the “power outage.”
*   **The participation pattern** can describe which citizens and houses were affected by the power outage and define their roles in the event.
*   **The explanation pattern** can combine the above pattern instances into a complete explanation, and it also allows for a competing explanation in which a “power plant failure” caused the outage. These two explanations can share the same “power outage” event instance while associating different causes.

<img src="/images/2411.16609v1/x1.jpg" alt="Example of applying the F model ontology" style="width:85%; max-width:450px; margin:auto; display:block;">
*(Note: Part (g) in the figure above shows how the causal relation pattern and participation pattern can be combined to describe a specific power outage event scenario.)*

### Comparison with Existing Models
Through comparative analysis with a variety of existing event models such as Eventory, CIDOC CRM, and EventML, the superiority of the F model is highlighted.


| Functional Requirement | Eventory | Event Ont. | CIDOC CRM | EventML | VERL | E | F (this paper) |
|---|---|---|---|---|---|---|---|
| (1) Object participation | ● | ● | ● | ● | ● | ● | ● |
| (2) Time | ● | ● | ● | ● | ● | ● | ● |
| (3) Space | ● | ● | ● | ● | ● | ● | ● |
| (4a) Part-whole relation | ○ | ○ | ○ | ◦ | ● | ○ | ● |
| (4b) Causal relation | ◦ | ○ | ○ | ◦ | ◦ | ○ | ● |
| (4c) Related relation | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ● |
| (5) Documentation support | ● | ◦ | ○ | ◦ | ● | ● | ● |
| (6) Event explanation | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ● |
*Caption: ● - Fully supported; ○ - Partially supported; ◦ - Not supported*

<img src="/images/2411.16609v1/x2.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

**Comparison conclusions**:
*   **Best-performing aspects**: The F model provides full support for all functional requirements. Its most notable advantage lies in the comprehensive modeling of **structural relations (part-whole, causal, related)** and **event explanation**, which are severely lacking in all other existing models.
*   **Performance of other models**: Existing models generally handle basic aspects such as object participation, time, and space well, but offer very limited support for more complex structural relations and subjective explanations.

### Summary
This paper successfully designed an event model, Event-Model-F, based on a foundational ontology and a pattern-driven approach. Through its unique modular design, especially its support for event structural relations and multiple explanations, the model significantly surpasses existing models and provides a solid formal foundation for building interoperable distributed event systems capable of understanding complex human experiences.