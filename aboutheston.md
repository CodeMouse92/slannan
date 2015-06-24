# Introduction #

The Heston Scale is the means by which bugs are given a priority. Inspired by the Fujita and Richter scales, bugs are given a rating on a scale of H-0 to H-5.
A project’s “scaled score” is the sum of all bugs on the Heston Scale. It changes the priority of a programmer from reducing the raw number of bugs to lowering the scaled score, which naturally shifts their attention to higher-rated bugs.


# Details #

**H-0:** This is reserved for ideas and future features. The “zero” rating allows for these items to be logged without impacting the program’s scaled score, and makes it easy to find them on list sorted by the H-scale.

**H-1:** These are bugs that are only marginally noticeable to the user, if at all. To the end user, these can also appear as minor but desirable features that were overlooked. Examples include:
  * An exception that has to be caught in code every time, but the user never sees.
  * A depreciated or inefficient block of code that increases the time it takes to save a file by a few seconds.
  * A platform incompatibility that requires a less-than-ideal workaround in the source code.

**H-2:** These bugs are more noticeable to the user, but don’t significantly interfere with their use of the program, and are generally ignorable. Examples include:
  * The screen flickers while scrolling down.
  * A button becomes momentarily unresponsive after a particular action.
  * An inefficient block of code that causes a moderate delay in saving a file (10-30 seconds).

**H-3:** Bugs with this rating are much more noticeable, and irritating enough to interfere with a user’s workflow, possibly prompting them to discontinue their use of the program. Examples include:
  * Repeated error messages on a common task (with task being completed).
  * Text blacking out when scrolling.
  * An important function becoming inaccessible after a particular action.
  * Significant delay in saving a file (30+ seconds)

**H-4:** This rating contains the more significant bugs, especially those that prevent completion of a task or use of a major or common feature. Examples include:
  * An error message that stops the creation of a new file.
  * An inability to see the font selection menu after a file is opened.
  * The “Find and Replace” function always seeking the word “txtFindValue” instead of the user’s requested search term.
  * The “Open Document” window closing itself whenever a folder is clicked on in it.
  * Displayed file data is corrupted (though the file itself remains unchanged.)

**H-5:** This is reserved for only the most significant bugs – ones that cause data loss or corruption, program freezes that require the user to kill the process or restart their machine, or CTDs (crash to desktop). Examples include:
  * The “Find and Replace” automatically and permanently erasing all instances of a user’s search term, instead of replacing with the specified “replace” term and allowing undo.
  * The “Redo” function permanently erasing the whole document.
  * File data is corrupted on file open, destroying the file.
  * Clicking the “Center” button freezes the program, requiring the user to kill the process.
  * Changing the font causes a CTD.