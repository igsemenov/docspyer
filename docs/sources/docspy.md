<!--
{
  "webtitle": "docspy \u2014 Docspy documentation"
}
-->

# docspy

Creates an overview of your Python code.

## docpackage()

<pre class="py-sign">docspy.<b>docpackage</b>(srcdir, docdir, mode, maxdepth=<span>None</span>) → <em>None</em></pre>

Generates documentation for a python package.

<b>Parameters</b>

<p><span class="vardef">● <code>srcdir</code> : <em>str</em></span></p>

<dl><dd>
  Path to the package directory.
</dd></dl>

<p><span class="vardef">● <code>docdir</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef">● <code>mode</code> : <em>str</em></span></p>

<dl><dd>
  Specifies the output format — <mark>&quot;html&quot;</mark> or <mark>&quot;md&quot;</mark>.
</dd></dl>

<p><span class="vardef">● <code>maxdepth</code> : <em>int</em></span></p>

<dl><dd>
  Maximum depth of the documentation tree.
</dd></dl>

## docscript()

<pre class="py-sign">docspy.<b>docscript</b>(srcfile, docdir, mode) → <em>None</em></pre>

Makes a report on a python script.

<b>Parameters</b>

<p><span class="vardef">● <code>srcfile</code> : <em>str</em></span></p>

<dl><dd>
  Path to the python script.
</dd></dl>

<p><span class="vardef">● <code>docdir</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef">● <code>mode</code> : <em>str</em></span></p>

<dl><dd>
  Specifies the output format — <mark>&quot;html&quot;</mark> or <mark>&quot;md&quot;</mark>.
</dd></dl>

## docsource()

<pre class="py-sign">docspy.<b>docsource</b>(srcpath, docpath, codeblocks=<span>False</span>) → <em>None</em></pre>

Converts an MD source file to an HTML page.

<b>Parameters</b>

<p><span class="vardef">● <code>srcpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the source file.
</dd></dl>

<p><span class="vardef">● <code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef">● <code>codeblocks</code> : <em>bool</em></span></p>

<dl><dd>
  Code highlighting is activated, if <i>True</i>.
</dd></dl>

## builddocs()

<pre class="py-sign">docspy.<b>builddocs</b>(srcpath, docpath, config=<span>None</span>) → <em>None</em></pre>

Assemble HTML documentation from MD source files.

<b>Parameters</b>

<p><span class="vardef">● <code>srcpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the source directory.
</dd></dl>

<p><span class="vardef">● <code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef">● <code>config</code> : <em>dict</em></span></p>

<dl><dd>
  Configuration parameters, see <code>docsconfig()</code>.
  If <i>None</i>, the default settings are used.
</dd></dl>

## docsconfig()

<pre class="py-sign">docspy.<b>docsconfig</b>() → <em>dict</em></pre>

Returns a template for setting configuration parameters of the documentation builder.

The template is a dictionary where:

- The keys are the parameters names.
- The values specify the default settings.

<b>Keys</b>

<p><span class="vardef">● <code>doclogo</code> : <em>str = ''</em></span></p>

<dl><dd>
  Documentation logo as an SVG or HTML tag.
  The recommended size is 30-40px.
</dd></dl>

<p><span class="vardef">● <code>codeblocks</code> : <em>bool = True</em></span></p>

<dl><dd>
  Code highlighting is activated, if <i>True</i>.
</dd></dl>

<p><span class="vardef">● <code>swaplinks</code> : <em>bool = False</em></span></p>

<dl><dd>
  If <i>True</i>, links to MD files are converted 
  to HTML ones across the source files.
</dd></dl>

<p><span class="vardef">● <code>extracss</code> : <em>str = ''</em></span></p>

<dl><dd>
  Custom CSS styles to include.
</dd></dl>

<p><span class="vardef">● <code>extrajs</code> : <em>str = ''</em></span></p>

<dl><dd>
  Custom JS code to include.
</dd></dl>

## docmodules()

<pre class="py-sign">docspy.<b>docmodules</b>(modules, docpath, hostname=<span>None</span>)</pre>

Creates MD documentation for a group of python modules.

<b>Parameters</b>

<p><span class="vardef">● <code>modules</code> : <em>list</em></span></p>

<dl><dd>
  List of python modules (objects)
</dd></dl>

<p><span class="vardef">● <code>docpath</code> : <em>str</em></span></p>

<dl><dd>
  Path where to place the output files.
</dd></dl>

<p><span class="vardef">● <code>hostname</code> : <em>str = None</em></span></p>

<dl><dd>
  Name of the modules holder (package, namespace, etc.)
  to set the webtitles of the output files.
</dd></dl>

## cleardocs()

<pre class="py-sign">docspy.<b>cleardocs</b>(dirpath)</pre>

Removes HTML, CSS, JS and MD files from a specified folder.

## clearcache()

<pre class="py-sign">docspy.<b>clearcache</b>(rootpath=<span>None</span>)</pre>

Removes content of <code>&lowbar;&lowbar;pycache__</code> folders in a directory tree.

<b>Parameters</b>

<p><span class="vardef">● <code>rootpath</code> : <em>str</em></span></p>

<dl><dd>
  Path to the root of the directory tree.
</dd></dl>