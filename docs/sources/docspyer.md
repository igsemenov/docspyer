<!--
{
  "webtitle": "Modules \u2014 docspyer documentation",
  "codeblocks": false
}
-->

# docspyer

High-level documentation tools.

## docpackage()

<pre class="py-sign">docspyer.<b>docpackage</b>(pkgpath, docpath, mode, maxdepth=<span>None</span>) → <em>None</em></pre>

Creates an overview of a python package (static analysis).

<b>Parameters</b>

<p><span class="vardef"><code>pkgpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the package directory.
</dd></dl>

<p><span class="vardef"><code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef"><code>mode</code> : <em>str</em></span></p>

<dl><dd>
  Specifies the output format — <i><mark>&quot;html&quot;</mark></i> or <i><mark>&quot;md&quot;</mark></i>.
</dd></dl>

<p><span class="vardef"><code>maxdepth</code> : <em>int = None</em></span></p>

<dl><dd>
  Maximum depth of nested subpackages.
  If <i>None</i>, all subpackages are included.
</dd></dl>

## docscript()

<pre class="py-sign">docspyer.<b>docscript</b>(filepath, docpath, mode) → <em>None</em></pre>

Creates a report on a python script (static analysis).

<b>Parameters</b>

<p><span class="vardef"><code>filepath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the python script.
</dd></dl>

<p><span class="vardef"><code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef"><code>mode</code> : <em>str</em></span></p>

<dl><dd>
  Specifies the output format — <i><mark>&quot;html&quot;</mark></i> or <i><mark>&quot;md&quot;</mark></i>.
</dd></dl>

## docsource()

<pre class="py-sign">docspyer.<b>docsource</b>(srcpath, docpath, codeblocks=<span>False</span>) → <em>None</em></pre>

Converts an MD source file to an HTML page.

<b>Parameters</b>

<p><span class="vardef"><code>srcpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the source file.
</dd></dl>

<p><span class="vardef"><code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef"><code>codeblocks</code> : <em>bool</em></span></p>

<dl><dd>
  Code highlighting is activated, if <i>True</i>.
</dd></dl>

## builddocs()

<pre class="py-sign">docspyer.<b>builddocs</b>(srcpath, docpath, **settings) → <em>None</em></pre>

Assemble HTML documentation from MD source files.

<b>Parameters</b>

<p><span class="vardef"><code>srcpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the source directory.
</dd></dl>

<p><span class="vardef"><code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef"><code>settings</code> : <em>dict</em></span></p>

<dl><dd>
  Configuration settings (see below).
</dd></dl>

<b>Settings</b>

<p><span class="vardef"><code>doclogo</code> : <em>str = None</em></span></p>

<dl><dd>
  Documentation logo as an SVG or HTML tag.
  The recommended size is 30-40px.
</dd></dl>

<p><span class="vardef"><code>codeblocks</code> : <em>bool = True</em></span></p>

<dl><dd>
  Code highlighting is activated, if <i>True</i>.
</dd></dl>

<p><span class="vardef"><code>swaplinks</code> : <em>bool = False</em></span></p>

<dl><dd>
  If <i>True</i>, links to MD files are converted 
  to HTML ones across the source files.
</dd></dl>

<p><span class="vardef"><code>extracss</code> : <em>str = None</em></span></p>

<dl><dd>
  Custom CSS styles to include (path or text).
</dd></dl>

<p><span class="vardef"><code>extrajs</code> : <em>str = None</em></span></p>

<dl><dd>
  Custom JS code to include (path or text).
</dd></dl>

## cleardocs()

<pre class="py-sign">docspyer.<b>cleardocs</b>(dirpath) → <em>None</em></pre>

Removes HTML, CSS, JS files from a specified folder.

## docmods()

<pre class="py-sign">docspyer.<b>docmods</b>(modules, docpath, **settings) → <em>None</em></pre>

Creates MD documentation for python modules.

<b>Parameters</b>

<p><span class="vardef"><code>modules</code> : <em>list</em></span></p>

<dl><dd>
  List of python modules (live objects).
</dd></dl>

<p><span class="vardef"><code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef"><code>settings</code> : <em>dict</em></span></p>

<dl><dd>
  Configuration settings (see below).
</dd></dl>

<b>Settings</b>

<p><span class="vardef"><code>docsname</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the index file.
  The file is omitted, if no name is given.
</dd></dl>

<p><span class="vardef"><code>hostname</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the modules holder. 
  If <i>None</i>, the longest common name is used. 
</dd></dl>

<p><span class="vardef"><code>npstyle</code> : <em>bool = True</em></span></p>

<dl><dd>
  Expects numpy style docstrings, if <i>True</i>.
  Otherwise, plain text format is used.
</dd></dl>

<p><span class="vardef"><code>moddocs</code> : <em>bool = True</em></span></p>

<dl><dd>
  If <i>False</i>, modules are not documented, 
  only the index file is processed.
</dd></dl>

<p><span class="vardef"><code>modrefs</code> : <em>bool = True</em></span></p>

<dl><dd>
  If <i>True</i>, the modules reference is added to the index file.
</dd></dl>

<p><span class="vardef"><code>clsverbs</code> : <em>int = 0</em></span></p>

<dl><dd>
  Controls the verbosity of classes (0-2)
  regarding the methods headings.
</dd></dl>

<p><span class="vardef"><code>codeblocks</code> : <em>bool = False</em></span></p>

<dl><dd>
  Code highlighting is activated, if <i>True</i>.
</dd></dl>

## funcstomd()

<pre class="py-sign">docspyer.<b>funcstomd</b>(*funcs, **settings) → <em>str</em></pre>

Returns documentation of functions in MD.

<b>Parameters</b>

<p><span class="vardef"><code>funcs</code> : <em>tuple</em></span></p>

<dl><dd>
  Functions to be documented.
</dd></dl>

<p><span class="vardef"><code>settings</code> : <em>dict</em></span></p>

<dl><dd>
  Configuration settings (see below).
</dd></dl>

<b>Settings</b>

<p><span class="vardef"><code>hostname</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the functions holder.
</dd></dl>

<p><span class="vardef"><code>level</code> : <em>int = None</em></span></p>

<dl><dd>
  Sets the level of functions headings.
</dd></dl>

<p><span class="vardef"><code>npstyle</code> : <em>bool = True</em></span></p>

<dl><dd>
  Expects numpy style docstrings, if <i>True</i>.
  Otherwise, plain text format is used.
</dd></dl>

## classtomd()

<pre class="py-sign">docspyer.<b>classtomd</b>(pycls, **settings) → <em>str</em></pre>

Returns a class documentation in MD.

<b>Parameters</b>

<p><span class="vardef"><code>pycls</code> : <em>type</em></span></p>

<dl><dd>
  Class to be documented.
</dd></dl>

<p><span class="vardef"><code>settings</code> : <em>dict</em></span></p>

<dl><dd>
  Configuration settings (see below).
</dd></dl>

<b>Settings</b>

<p><span class="vardef"><code>hostname</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the class holder.
</dd></dl>

<p><span class="vardef"><code>level</code> : <em>int = None</em></span></p>

<dl><dd>
  Specifies the level of the class heading.
</dd></dl>

<p><span class="vardef"><code>npstyle</code> : <em>bool = True</em></span></p>

<dl><dd>
  Expects numpy style docstrings, if <i>True</i>.
  Otherwise, plain text format is used.
</dd></dl>

<p><span class="vardef"><code>verbosity</code> : <em>int = 0</em></span></p>

<dl><dd>
  Controls the class verbosity (0-2)
  regarding the methods headings.
</dd></dl>

<p><span class="vardef"><code>predicate</code> : <em>function = None</em></span></p>

<dl><dd>
  Function that filters class methods.
  If <i>None</i>, only public methods with docs are retained.
</dd></dl>

## funcstable()

<pre class="py-sign">docspyer.<b>funcstable</b>(funcs, hostdoc=<span>None</span>, indent=<span>None</span>) → <em>str</em></pre>

Returns functions overview as an MD table.

<b>Parameters</b>

<p><span class="vardef"><code>funcs</code> : <em>list</em></span></p>

<dl><dd>
  Functions to be inspected.
</dd></dl>

<p><span class="vardef"><code>hostdoc</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the parent MD document.
  If given, links to functions are generated.
</dd></dl>

<p><span class="vardef"><code>indent</code> : <em>int = None</em></span></p>

<dl><dd>
  Specifies the table indent, if needed.
</dd></dl>

## classfuncs()

<pre class="py-sign">docspyer.<b>classfuncs</b>(pycls, predicate=<span>None</span>) → <em>list</em></pre>

Fetches methods from a class.

<b>Parameters</b>

<p><span class="vardef"><code>pycls</code> : <em>type</em></span></p>

<dl><dd>
  Class to be inspected.
</dd></dl>

<p><span class="vardef"><code>predicate</code> : <em>function = None</em></span></p>

<dl><dd>
  Function that filters class methods.
  If <i>None</i>, only public methods with docs are retained.
</dd></dl>

<b>Returns</b>

<p><span class="vardef"><em>list</em></span></p>

<dl><dd>
  List with the selected methods.
</dd></dl>

## npdocasmd()

<pre class="py-sign">docspyer.<b>npdocasmd</b>(docstr) → <em>str</em></pre>

Converts a numpy style docsrting to MD.

<b>Parameters</b>

<p><span class="vardef"><code>docstr</code> : <em>str</em></span></p>

<dl><dd>
  Docstring to be converted.
</dd></dl>

<b>Returns</b>

<p><span class="vardef"><em>str</em></span></p>

<dl><dd>
  The resulting docstring in MD.
</dd></dl>

## DocFormat

<pre class="py-sign"><b><em>class</em></b> docspyer.<b>DocFormat</b>()</pre>

Custom formatter of source files.

<pre class="py-sign">DocFormat.<b>setconfig</b>(<em>self</em>, srcdirs, hostmod)</pre>

Sets up the formatter.

<b>Parameters</b>

<p><span class="vardef"><code>srcdirs</code> : <em>list[str]</em></span></p>

<dl><dd>
  Folders to search for source files.
</dd></dl>

<p><span class="vardef"><code>hostmod</code> : <em>module</em></span></p>

<dl><dd>
  Module used to run inline calls.
</dd></dl>