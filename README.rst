Overview
====================

Comparing document versions to identify changes is a common approach to
the review process. Many software programs, i.e., diff tools, exist precisely
for this purpose, however, their effectiveness is highly-dependent on the
document format, with plain text files being the easiest to compare.
SISTEMA uses XML to store its project content, which can be compared,
yet its internal structure makes interpreting the results quite challenging.

ssm2txt is a small utility to assist in comparing SISTEMA projects by
converting them to plain, line-oriented text, structured in a manner similar
to the presentation used by the SISTEMA GUI. These text files can then be
compared with any standard diff tool to identify modifications.

It is important to note that ssm2txt does not duplicate any evaluation or
computation normally performed by SISTEMA; its aim is solely to convert
XML content into text. This is most notably evident in the output containing
content not visible in SISTEMA due to specific settings. For example, SISTEMA
hides the PLr graph when a safety function's PLr is entered directly.
The PLr graph settings are always present in the file, regardless of the
selected PLr determination method, so ssm2txt includes them in its output.
This should not present a problem in the context of file comparison since
the hidden content will not be flagged by a diff tool if it does not change.


Prerequisites
====================

1. Python, version 3.x.

2. SISTEMA, version 2.x. Technically, ssm2txt will run without SISTEMA,
   i.e., it doesn't directly interact with SISTEMA, but SISTEMA is required
   to create the source project.

3. A diff tool. Not an absolute requirement, although the output of this
   program is intended for use with one. No special requirements other
   than supporting UTF-8 encoded files.


Usage
====================

ssm2txt is a command-line utility, executed as follows::

  python -m ssm2txt <path to ssm>

The output text file will have the same path and name as the source SISTEMA
project file, but with a txt extension.
