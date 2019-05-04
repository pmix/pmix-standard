[![Build Status](https://travis-ci.org/pmix/pmix-standard.svg?branch=master)](https://travis-ci.org/pmix/pmix-standard)

# PMIx Standard

This repository contains the LaTeX source for the PMIx Standard document, and discussions regarding the PMIx standard.

Contributions of any form (e.g., use cases, questions, suggestions) are encouraged from anyone interested in the evolution of the PMIx Standard.
You can participate in the discussion on the [PMIx Forum mailing list](https://groups.google.com/group/pmix-forum),
on the regular teleconference (announced on the mailing list), or the Pull Requests/Issues
on this GitHub repository.

The community relies on Issues and Pull Requests to discuss changes to the standard for
a few reasons. First, it provides an archive of the conversation around a change to the
standard that can be vital in understanding the rationale for the change if that conversation
needs to be revisited in the future. Next, it facilitates asynchronous conversation from
a geographically distributed user-base. To that end, any discussion on the teleconference
about specific Issues or Pull Requests will be noted as a comment to that Issue or Pull Request. Lastly, the GitHub mechanism also serves as our consensus building medium for accepting changes
once all dissenting opinions and questions have been resolved, providing an archive of
the responses to those concerns and those individuals participating in the process.


## Standardization Process

The PMIx standardization process considers contributions by using the general workflow outlined below:

 1. Open a **GitHub Issue** describing your contribution for general discussion.
 2. Open a **GitHub Pull Request (PR)** if a specific change to the PMIx Standard is needed.
    * Reference the corresponding Issue(s). Keep the PR marked as [Draft PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/) until an implementation is available and the PR is ready for broader discussion.
    * Send an email to the [PMIx Forum mailing list](https://groups.google.com/forum/#!forum/pmix-forum) once the PR is ready for discussion.
    * Once the discussion has resolved (i.e., dissenting opinions and questions have been addressed) then it can move to an official "Reading" in the next teleconference. Email the mailing list once it is ready for "Reading" to have it added to the teleconference agenda.
 3. Official "**Reading**" of the PR during a teleconference
    * If no revisions are required or objections raised (either on the PR or in the teleconference) then the PR can be considered for "Acceptance" in the next teleconference.
 4. Official "**Acceptance**" of the PR during a following teleconference
    * If no objection is raised (either on the PR on in the teleconference) then the PR is merged into the document and, if also resolved, the corresponding Issue is closed.

**General Statements:**

 * Any individual or organization may participate in the discussion on a topic.
 * Regular teleconferences are announced on the PMIx Forum mailing list
   - Teleconferences provide a high bandwidth discussion format for various topics
     surrounding the PMIx Standard, and a synchronization mechanism to guide progress.
   - Notes from the teleconferences will be archived on the PMIx Forum wiki.
   - Specific notes regarding an Issue or PR from the teleconference will be made
     on that Issue or PR directly immediately following the teleconference.
 * The PMIx Forum mailing list may be used for questions about the PMIx Standard.
   The PMIx community may request that you open a corresponding Issue if the question
   may require clarifications or other modifications to the PMIx Standard.


### Phase 1: GitHub Issue for discussion

 * A GitHub Issue must be opened for any contribution to the PMIx Standard.
   - For example, the Issue might describe a use case that is requesting support,
     a clarification to the document, a new specific interface, or a question about
     existing behavior.
 * The Issue provides a discussion forum for the contribution without the requirement
   of specific changes to the PMIx Standard document.
 * Once an Issue is ready for discussion it is helpful, though not required, to send a message to the PMIx Forum mailing list to raise awareness.
 * If a PMIx Standard change is required then a Pull Request must be created (See Phase 2).
    - Multiple Pull Requests may reference a single Issue.
 * The Issue will be closed once it has been resolved by the "**Acceptance**" of the
   associated PRs or once the participants are satisfied with the conversation.
   

### Phase 2: GitHub PR for specific changes

 * When a specific change to the PMIx Standard is required a PR
   must be opened with a reference to the corresponding Issue(s).
 * When the PR is opened it should be placed in a [Draft PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/) state until the following conditions
   are met:
   - The contents of the PR are ready for review and broad discussion with the PMIx community.
   - If necessary, an open-source implementation of the proposal is available.
     Reference to the implementation must be included in the PR.
 * Once the [Draft PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/) designation is removed then only new commits are permitted on the branch.
   - The branch associated with the PR must not be squashed or force pushed after this point.
   - This preserves the timeline of changes in relationship to the discussion that may occur on the PR.
 * Once all dissenting opinions and questions have been resolved, then the PR may be presented for a formal "**Reading**" during the next teleconference.
   - The author(s) must send an email to the PMIx Forum mailing list when they are ready to present the PR for "**Reading**" at least 4 days before the next teleconference.
   - The PR(s) scheduled for "**Reading**" will be noted in the teleconference agenda sent out before the meeting.
   - A "**Straw Poll**" comment is placed on the PR once the "**Reading**" announcement email has been sent out by the author(s).
     - The "**Straw Poll**" provides the community with a sense of how many people have viewed the PR and are following the discussion. This serves no official purpose other than to help define participation in the consensus building process.
     - Those participants that approve the "**Reading**" must indicate that by placing a :+1: emoji on the comment.
     - Those participants that have specific concerns regarding the "**Reading**" must indicate that by placing a :-1: emoji on the comment.
         - Anyone indicating concern must provide a comment on the ticket following the "**Staw Poll**" comment. The author(s) can then work to address the concern.
     - Participation in the "**Straw Poll**" starts when the comment is posted and concludes after the teleconference where the PR is presented for "**Reading**"


### Phase 3: GitHub PR "Reading"

 * One of the author(s) (or someone designated by them) must be present on the teleconference to present the PR for "**Reading**" and discussion.
 * In the teleconference, the presenter will discuss the PR and address any questions raised.
   - During the presentation someone will be designated to take notes on the PR (and/or Issue) for the presenter.
   - These notes will declare if the PR is eligible for "**Acceptance**" in the next teleconference.
     - The PR is eligible for "**Acceptance**" if no revisions are required, there are no unanswered questions (either on the PR or in the teleconference), or no objections raised (either on the PR or in the teleconference).
 * The PR may be voluntarily closed as "**Withdrawn**" by the corresponding author(s) for any reason. For example, if a dissenting opinion is raised that cannot be resolved in the scope of that PR.
 * If revisions are required or further discussion is needed then the interested parties should continue discussion on the PR.
   - If no changes to the PR result from the discussion then the PR can be considered for "**Acceptance**" without the need for another "**Reading**".
   - If changes are made to the PR (with reasonable exceptions for minor spelling/grammar changes) then another "**Reading**" must be scheduled (See Phase 2) to allow interested parties to review the changes. This will include another "**Straw Poll**".
   - If major changes are required to the PR the author(s) should consider a separate, replacement PR, and marking the original PR as "**Withdrawn**".
 * If no dissent is voiced then the PR can be considered for "**Acceptance**" as early as the next teleconference.
   - The author(s) must send an email to the PMIx Forum mailing list when they wish the PR to be considered for "**Acceptance**" at least 4 days before the next teleconference.
   - The PR(s) scheduled for "**Acceptance**" will be noted in the teleconference agenda sent out before the meeting.
   - A "**Straw Poll**" comment is placed on the PR once the "**Acceptance**" announcement email has been sent out by the author(s).
     - Participation in the "**Straw Poll**" starts when the comment is posted and concludes immediately after the teleconference where the PR is presented for "**Acceptance**"


### Phase 4: GitHub PR "Acceptance"

 * Between the successful "**Reading**" teleconference and the scheduled "**Acceptance**" teleconference discussion on the PR may continue.
   - From those discussions, all dissenting options and questions must be resolved.
 * One of the author(s) (or someone designated by them) must be present on the teleconference to present the PR for "**Acceptance**".
   - Someone will be designated to take notes on the PR (and/or Issue) for the presenter.
 * If no objection is voiced then the PR is "**Accepted**" into the PMIx Standard and the PR is merged immediately.
   - The authors will followup on the Issue to determine if it is resolved or needs more work before resolving it.


### Phase 5: Celebration!

 * Thank you for participating in the PMIx standardization process!


## Building the PMIx Standard document

You will need a LaTeX installation on your system.
To build simply type `make` and it will generate the standard PDF.
See documentation in header comment of `pmix-standard.tex`, and the macros provided by `pmix.sty`.
