# Get Out The Vote - June 2016

**Category:** Number Theory / Logic
**URL:** https://www.janestreet.com/puzzles/get-out-the-vote-index/

## Problem Statement

Primary elections in the micro-state of Neverland!

This state follows the following rules: let D be the number of delegates to be elected, N the total number of votes and Xi the number of ballots cast for each candidate i. Initially, each candidate gets assigned Floor(D * Xi/N) delegates where Floor() is the standard floor function. Then, the remaining delegates (if any) get assigned in decreasing order of the remainders D * Xi/N – Floor(D * Xi/N). That is, if there are K remaining delegates, the K candidates who have the largest remainders D * Xi/N – Floor(D * Xi/N) will each receive a delegate.

After counting the votes, 102 ballots were found, none of which were invalid or void, and the only three candidates Harry, Larry, and Mary got assigned 2, 2, and 3 delegates respectively.

Later on, an audit commission found two mistakes were made:

1. There were 8 delegates to assign, not 7.
2. A 103rd ballot had been missed, with an extra vote for Harry.

After correcting for those errors, the final results show that Harry lost one delegate.

Harry is outraged! How could this happen?? How many votes did each candidate receive in this election?
