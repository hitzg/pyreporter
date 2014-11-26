
import pyreporter
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update(pyreporter.rcParams)


def myplot(fancy_args):
    # some size specification for the aspect ration (could also be (16,6))
    fig = plt.figure(figsize=(8,3)) 
    x = np.linspace(0,2*np.pi, 100)
    y = np.cos(x)
    plt.plot(x,y,'b')
    return fig

pdf = pyreporter.Report('test', '/tmp/pyreptest', author='Gregory', 
        title="A simple pyreporter example", pagesize='a4paper',left='2cm', 
        right='2cm')
pdf.force_all = True




pdf.add_section('First part $x$')
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

pdf.add_subsection('Plots!')

the_fancy_argument = None
myplotgenerator = lambda: myplot(the_fancy_argument) 
pdf.add_plot(fig=myplotgenerator, widthratio=0.8, name='plot1', 
        caption=r'A nice plot')

pdf.add_plot(fig=myplotgenerator, widthratio=0.4, name='plot2')

pdf.add_subsection('Table with awesome results')
header = [pyreporter.bold(r) for r in['value1','value2','value3']]
data = np.random.randint(0,10,(4,3))
data = [[str(y) for y in x] for x in data]
pdf.add_table(data, header=header, cols='lcr', caption='a very nice table')

pdf.close(build=True)
