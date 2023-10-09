<!--
{
  "webtitle": "docspy.inspect \u2014 Docspy documentation"
}
-->

# docspy.inspect

Utilities for exploring python scripts.

## modtomd()

<pre class="py-sign">docspy.inspect.<b>modtomd</b>(pymod, meta=<span>None</span>) → <em>str</em></pre>

Dumps functions and classes from a module in MD format.

<b>Parameters</b>

<p><span class="vardef">● <code>pymod</code> : <em>module</em></span></p>

<dl><dd>
  A python module to be documented.
</dd></dl>

<p><span class="vardef">● <code>meta</code> : <em>dict</em></span></p>

<dl><dd>
  Metadata added as a header to the output document.
  If the argument is not empty or <i>None</i>, it is formatted 
  as a JSON string enclosed by an HTML comment.
  Otherwise, the argument is ignored.
</dd></dl>

<b>Returns</b>

<p><span class="vardef"><em>str</em></span></p>

<dl><dd>
  The resulting MD document.
</dd></dl>

## modtorst()

<pre class="py-sign">docspy.inspect.<b>modtorst</b>(pymod) → <em>str</em></pre>

Dumps functions and classes from a module in RST format.

<b>Parameters</b>

<p><span class="vardef">● <code>pymod</code> : <em>module</em></span></p>

<dl><dd>
  A python module to be documented.
</dd></dl>

<b>Returns</b>

<p><span class="vardef"><em>str</em></span></p>

<dl><dd>
  The resulting RST document.
</dd></dl>

## getscripts()

<pre class="py-sign">docspy.inspect.<b>getscripts</b>(dirpath)</pre>

Extracts python scripts from a specified folder.

<b>Parameters</b>

<p><span class="vardef">● <code>dirpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the folder with the scripts.
</dd></dl>

<b>Returns</b>

<p><span class="vardef"><em>Scripts</em></span></p>

<dl><dd>
  Object that holds script records.
</dd></dl>

## Scripts

<pre class="py-sign"><b><em>class</em></b> docspy.inspect.<b>Scripts</b>()</pre>

Represents python scripts fetched from a certain folder.

<b>Attributes</b>

<p><span class="vardef">● <code>dirpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the folder with the scripts.
</dd></dl>

<p><span class="vardef">● <code>scripts</code> : <em>dict</em></span></p>

<dl><dd>
  Namespace of the scripts (name-to-record).
</dd></dl>

### listscripts()

<pre class="py-sign">Scripts.<b>listscripts</b>(<em>self</em>) → <em>list[str]</em></pre>

Returns names of the scripts.