pyreporter
==========

Simple tool to create latex reports from python.

`pyreporter` has simple function to add blocks of latex to an output file. It also features functions to directly add [matplotlib](http://matplotlib.org/) plots and automatically resizes them, so that fontsizes and linewidths match the document.

The emphasis here lies on simplicity rather than flexibility and design customization.

### A Short Howto:

1. Start your report:
```python
pdf = pyreporter.Report('test', '/tmp/pyreptest', author='Gregory', 
              title="A simple pyreporter example", pagesize='a4paper',
              left='2cm', right='2cm')
```
2. Your good to go: add some content
```python
pdf.add_text("""Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor
sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed
diam voluptua.""")
pdf.add_equation(r'x =\left[\begin{matrix} 1 & 2 \\ 3 & 4 \end{matrix}\right]')
pdf.add_text("""At vero eos et accusam et justo duo dolores et ea rebum.
Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor
sit amet.""")
```
3. Now lets add a plot:
```python


fig = plt.figure(figsize=(8,3)) 
x = np.linspace(0,2*np.pi, 100)
y = np.cos(x)
plt.plot(x,y,'b')

pdf.add_plot(fig=fig, widthratio=0.8, name='plot1', caption='A nice plot')
```
4. And also a table.
```python
header = ['value1','value2','value3']
data = np.random.randint(0,10,(4,3))
data = [[str(y) for y in x] for x in data]
pdf.add_table(data, header=header, cols='lcr', caption='a very nice table')
```
5. Finally close the report and build the pdf:
```python
pdf.close(build=True)
```

