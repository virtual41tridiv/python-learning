The pilot will answer two questions: **Can we correct more label errors for the same expert time? Do those corrections improve water mapping on unseen flood events?**

The first deliverable is evidence that the audit strategy is useful. Improved model performance is a separate result to measure.

Use the following scope for the first six weeks:

| Decision | Pilot choice |
|---|---|
| Dataset | Sen1Floods11 |
| Mapping target | Water present at satellite acquisition time |
| Training events | At least four eligible source events, subject to reference availability |
| Validation and testing | Separate events for tuning and final testing; aim for at least two held-out test events |
| Audit units | Initially 128 × 128 pixels; finalize after checking annotation cost |
| Initial audit | Approximately 60 blocks, randomly sampled across context groups |
| Main model | One tuned U-Net using Sentinel-1 VV/VH |
| Comparison methods | Proposed allocation, context-stratified random sampling, Active WeaSuL and active label cleaning |
| Later extensions | Additional architectures, external datasets, a second segmentation task and formal theoretical guarantees |

If suitable events cannot support this separation, reduce the claims and redesign the pilot before running the comparison.

Gather these inputs before annotation begins:

| Required data | Acceptance check | Responsible role |
|---|---|---|
| Sentinel-1 images and event metadata | Locations, dates and image channels are available and consistent | Data engineer |
| Sentinel-1 and Sentinel-2 weak labels | Their construction rules and source relationships are documented | Data engineer + research lead |
| Pre-event vegetation and observation-quality information | Available consistently enough to define a small number of groups | Remote-sensing lead |
| Independent reference evidence | Timing, alignment and ability to resolve water are checked for each candidate event | Remote-sensing lead |
| Existing hand labels | Stored separately and hidden when used for simulated audits or testing | Evaluation owner |
| Annotation records | Store corrected labels, validity masks, evidence, time and label versions | Data engineer |

Do not assume that the released hand-labeled and weak-labeled subsets contain matching chips. Where necessary, reproduce weak labels on hand-labeled chips using documented rules.

Before auditing, freeze a short annotation guide. It must define water, non-water, mixed pixels, acceptable evidence and unresolved pixels. Establish a consistent rule for ending an unproductive inspection. An unresolved attempt still consumes annotation time.

Assign people to these responsibilities. One person may hold several roles, but keep final evaluation labels inaccessible to the people tuning acquisition and training.

| Role | Accountable for |
|---|---|
| Research lead | Scope, comparison protocol, budget and proceed/stop decisions |
| Remote-sensing lead | Reference suitability, label definitions and interpretation guidance |
| Two interpreters | Annotation; independent labeling of a subset |
| Adjudicator | Resolving interpreter disagreements where evidence permits |
| ML/data engineer | Data preparation, audit policies, U-Net training and reproducibility |
| Evaluation owner/statistical reviewer | Hidden assessment data, fair comparisons and uncertainty analysis |

Plan the expert effort as follows. These are **person-hours**, so two people reviewing the same block both consume time.

| Activity | Suggested allowance |
|---|---:|
| Reference screening and annotation-guide preparation | 10 hours |
| Shared initial audit of approximately 60 blocks | 15 hours |
| Additional acquisition: four methods × 10 hours | 40 hours |
| Independent assessment collection | 15 hours |
| Second interpretation and adjudication | 10 hours |
| Contingency | 10 hours |
| **Total** | **100 hours** |

The 60-block estimate assumes approximately 15 minutes per initial inspection. Measure actual time immediately and revise the plan if this is unrealistic.

For the acquisition comparison, each method receives the same initial audit and the same additional 10-hour allowance. Charge any method-specific verification needed to obtain usable labels consistently. Keep research assessment costs separate and disclose them.

Track two budgets: actual project expenditure and the annotation time charged to each experimental method. If two methods request the same block, a blinded annotation can be reused, but both methods must be charged its recorded cost. Neither method may see it before selecting that block.

Engineering effort, GPU usage and any paid imagery are additional costs. Measure one representative training run before setting the compute allowance.

Carry out the work in five stages:

1. **Week 1: establish data and reference feasibility.**  
   Inventory candidate events, inspect reference coverage, assign training/validation/test events, and prepare the annotation guide. Record where evidence is missing; do not choose only locations already known to be easy to interpret.

   **Deliverable:** an event inventory, fixed split and annotation protocol.

2. **Week 2: complete the shared initial audit.**  
   Sample approximately 60 blocks across the eligible training events and a small number of context groups. Include unanimous-dry blocks as well as disagreement patterns. Start with roughly four to six groups to avoid dividing the small pilot into too many categories.

   Independently double-label a prespecified subset—for example, 20%—and adjudicate disagreements. Initially hide model predictions and weak labels from interpreters; compare with weak labels afterward.

   **Deliverable:** verified error examples, unresolved fractions, correction yield and observed annotation costs.

   **Decision:** release the main audit budget only if the target errors can be independently established and the remaining comparison is affordable. If shared omissions cannot be verified, revise the research claim.

3. **Weeks 3–4: compare acquisition methods.**  
   First debug the policies using controlled corruptions and hidden existing labels. These exercises test behavior relative to known or released labels; they do not prove real reference errors.

   Then run the four acquisition methods with the same candidate pool, starting labels, context, reference access and time allowance. Give each method its own label state and history.

   For the proposed method, estimate correctable area and time by group, use conservative priorities, and retain the proposed 20% exploration. Update in small batches using a schedule fixed before comparison.

   **Deliverable:** correction-versus-time curves and an auditable selection log for each method.

4. **Week 5: test the effect on learning.**  
   Train the same U-Net configuration using unchanged weak labels and labels produced by each acquisition method. Include trusted-only training if compute permits.

   Keep sensor inputs, training schedule, loss settings and tuning allowance matched. Use three paired training seeds where feasible. Exclude unresolved pixels from supervised loss.

   **Deliverable:** water IoU, water recall and dry-land false-positive rates for each held-out event.

5. **Week 6: assess results and decide the next experiment.**  
   Use the separate assessment collection to estimate remaining label error. Set its sample size and allocation using initial-pilot variability and cost before inspecting final comparative results.

   Report uncertainty using blocks/events rather than treating pixels as independent. Treat a result from only a few events as preliminary.

   **Deliverable:** a short decision report, corrected masks, audit records, reproducible configurations and representative success/failure examples.

Fix the success criteria before the main comparison:

| Question | Proposed decision criterion |
|---|---|
| Is the problem observable? | Independently verified shared errors recur across at least two source events. This is a feasibility signal, not a population-wide prevalence claim. |
| Is the audit process workable? | Actual inspection costs and unresolved rates allow the matched comparison to fit the remaining budget. |
| Is the method practically promising? | Target at least **20% more net corrected area at the same total annotation time** than the strongest baseline. This is a suggested minimum useful improvement, not a predicted result. |
| Is the evidence convincing? | Report the gain and its uncertainty. A positive estimate with a wide interval supports a larger study, not a demonstrated advantage. |
| Are improvements legitimate? | Gains survive adjudication, count introduced errors against corrections, and do not arise from deleting difficult pixels or changing the target definition. |
| Does learning improve? | Suggested target: at least **2 percentage points higher event-mean water IoU** than unchanged-label training, with recall and false positives reported. Also compare against the strongest acquisition baseline. |

If a baseline has zero or negative net corrections, report absolute differences rather than a misleading percentage improvement.

Interpret the outcomes separately:

- **Better correction yield and better mapping:** proceed to broader event validation.
- **Better correction yield but no mapping improvement:** retain the label-quality result and investigate why learning did not benefit.
- **An existing method performs equally well:** favor that method and narrow the novelty claim.
- **Independent evidence cannot resolve the target errors:** revise the data or target before developing a more elaborate allocation algorithm.

At the team meeting, settle five items: who owns each role, which events have usable reference evidence, whether 100 expert hours is affordable, what improvement would justify expansion, and the date of the first feasibility review.