
# -*- coding: utf-8 -*-
import string
import datetime
import random as rnd
import os


rcParams = {'text.usetex' : True,
          'text.latex.preamble':
                        [r"\usepackage{lmodern}", r"\usepackage{amsmath}"],
          'font.size' : 10,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          'lines.linewidth': 0.5,
          'axes.titlesize': 'large',
          'axes.linewidth': 0.3,
          'xtick.major.width': 0.25,
          'ytick.major.width': 0.25,
          'grid.linewidth': 0.125,
          'grid.linestyle': ':',
          'grid.color': [0.5, 0.5, 0.5],
          'legend.borderaxespad': 0.1,
          'legend.fontsize': 8,
          'legend.frameon': True,
          'xtick.minor.size': 1,
          'ytick.minor.size': 1,
          'xtick.major.size': 2,
          'ytick.major.size': 2,
          'figure.autolayout':True,
          'savefig.dpi': 300,
          'savefig.bbox': 'tight',
          'savefig.pad_inches': 0.01
          }

papersizes_wh_cm = dict(
        a0paper=(84.1,  118.9),
        a1paper=(59.4,  84.1),
        a2paper=(42.0,  59.4),
        a3paper=(29.7,  42.0),
        a4paper=(21.0,  29.7),
        a5paper=(14.8,  21.0),
        a6paper=(10.5,  14.8),
        b0paper=(100.0, 129.7),
        b1paper=(70.7,  100.0),
        b2paper=(50.0,  70.7),
        b3paper=(35.3,  50.0),
        b4paper=(25.0,  35.3),
        b5paper=(17.6,  25.0),
        b6paper=(12.5,  17.6),
        letterpaper=(21.59,27.94),
        legalpaper=(21.59,35.56),
        executivepaper=(18.41,26.6))


def almost_equal(a,b, tol=1e-8):
    """Helper function to compare floats"""
    return abs(a-b) <= (abs(a)+abs(b))/2. * tol

class Length(object):
    """ A class to handle lengths in a certain unit and convertions thereof. It
    supports 'm', 'cm', 'mm' and 'in'. Trough the attribute 'dpi' it also
    converts to and from 'pt'.
    """
    def __init__(self, *args, **kwargs):
        self.dpi = kwargs.get('dpi', 72.)
        if len(args) == 1:
            if type(args[0]) == str:
                self.from_string(args[0])
            else:
                self.value = float(args[0])
                self.unit = 'cm'
        elif len(args) == 2:
            self.value = float(args[0])
            self._valid_unit(args[1])
            self.unit = args[1]
        else:
            raise Exception('Length takes 1 or 2 arguments')
    
    def _valid_unit(self, u):
        if u not in ['pt','in', 'cm', 'mm', 'm']:
            raise Exception('Unknown length unit: {}'.format(su))

    def from_string(self, s):
        """ Assigns the value and unit from a string. Valid strings start with
        a value and are followed by a known unit
        """
        s = s.strip(' ')
        sv = s.rstrip(string.ascii_letters).strip(' ')
        su = s[len(sv):].strip(' ')
        self._valid_unit(su)
        self.value = float(sv)
        self.unit = su

    def convert_to(self, u):
        """Convert to the unit specified in by u.
        """
        v = self.get_value_in(u)
        return Length(v,u)

    def get_value_in(self, u):
        """Return the value of self in the unit u as a float
        """
        self._valid_unit(u)
        conversions = {'pt': self.dpi, 'cm': 2.54, 'mm': 25.4, 'm':
                0.0254, 'in': 1.}
        # convert to inch and then to desired unit
        return conversions[u]/conversions[self.unit]*self.value

    def __eq__(self,other):
        if (type(other)==Length):
            a = self.convert_to('in')
            b = other.convert_to('in')
            return almost_equal(a.value, b.value) 
        else:
            msg = "Unsupported operand type(s) for ==: '{}' and '{}'"
            raise TypeError(msg.format('Length', str(type(other))))

    def __mul__(self, other):
        if (type(other)==int or type(other)==float):
            return Length(self.value*other, self.unit)
        else:
            msg = "Unsupported operand type(s) for *: '{}' and '{}'"
            raise TypeError(msg.format('Length', str(type(other))))

    def __rmul__(self, other):
        if (type(other)==int or type(other)==float):
            return Length(self.value*other, self.unit)
        else:
            msg = "Unsupported operand type(s) for *: '{}' and '{}'"
            raise TypeError(msg.format(str(type(other)), 'Length'))

    def __div__(self, other):
        if (type(other)==int or type(other)==float):
            return Length(self.value/other, self.unit)
        else:
            msg = "Unsupported operand type(s) for /: '{}' and '{}'"
            raise TypeError(msg.format('Length', str(type(other))))

    def __repr__(self):
        return '{}{}'.format(self.value, self.unit)




class StandardTemplate:
    """ Class that serves as a namespace. Collects string templates and
    functions to build templates. This class could be inherited to create
    different styles
    """

    head = string.Template(
r"""\documentclass[$pagesize,$fontsize]{article}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[$pagesize,$orientation,left=$left,right=$right,top=$top,bottom=$bottom]{geometry}
\usepackage{caption}
\usepackage{booktabs}

\title{$title}
\author{$author}
\date{$date}
\begin{document}
\maketitle
""")

    tail = \
r"""
\end{document}
"""

    image = string.Template(
r"""
\includegraphics[$dimension=$size]{$fname}
""")

    @classmethod
    def float_wrapper(cls, realfloat=False, caption=False):
        """Creates a latex-float or a minipage. Minipages allow to place
        figures and tables exactly where they are entered in the tex file
        """
        part2 = list()
        if realfloat:
            part1 = ['']
            part1.append(r'\begin{$floattype}[H]')
            part1.append(r'  \centering')
            if caption:
                part2.append(r'  \caption{$caption}')
            part2.append(r'\end{$floattype}')
        else:
            part1 = ['']
            part1.append(r'\noindent%')
            part1.append(r'\begin{minipage}{\linewidth}%')
            part1.append(r'\vspace{0.3cm}')
            part1.append(r'\makebox[\linewidth]{%') 
            part2.append("}")
            if caption:
                part2.append(r'\captionof{$floattype}{$caption}')
            part2.append(r'\vspace{0.3cm}')
            part2.append(r'\end{minipage}')
        part2.append('')
        return '\n'.join(part1), '\n'.join(part2)


    @classmethod
    def figure(*args, **kwargs):
        hascaption = kwargs.has_key('caption')
        realfloat = kwargs.pop('float', False)
        pre, suf = Template.float_wrapper(realfloat, hascaption)
        middle = r'  \includegraphics[$dimension=$size]{$fname}'
        template = string.Template('\n'.join([pre, middle, suf]))
        return template.substitute(floattype='figure', **kwargs)
        
    @classmethod
    def section(*args,**kwargs):
        s ='\n'+ r'\$sectiontype$star{$sectiontitle}' + '\n'
        params = {'star': '*' if kwargs.pop('starred',False) else ''}
        if kwargs.pop('newpage',False):
            s = '\\newpage\n' + s
        params.update(kwargs)
        return string.Template(s).substitute(**params)

    @classmethod
    def table(cls, cols=None, **kwargs):
        hascaption = kwargs.has_key('caption')
        realfloat = kwargs.pop('float', False)
        pre, suf = Template.float_wrapper(realfloat, hascaption)
        data = kwargs.pop('data')
        header = kwargs.pop('header',None)
        kwargs['cols'] = 'l'*len(data[0]) if cols is None else cols
        middle = [r'\begin{tabular}{$cols}',r'  \toprule']
        if header is not None:
            middle.append('  ' + ' & '.join(header).replace('$','$$') + r'\\')
            middle.append(r'  \midrule')
        for i in data:
            middle.append('  ' + ' & '.join(i).replace('$','$$') + r'\\')
        middle.extend([r'  \bottomrule', r'\end{tabular}'])
        template = string.Template('\n'.join([pre]+middle+[suf]))
        return template.substitute(floattype='table', **kwargs)

    equation = string.Template(\
r"""\begin{equation}
$equation
\end{equation}
""")


#For now, we choose the standard template
Template = StandardTemplate


def make_table(data, cols=None, header=None, **kwargs):
    """Creates a tex block for a table

    Parameters
    ----------
    data: list
        A list of lists of strings that defines the the elements of the table.
        The lists are interpreted as a list of rows.
    cols: str, optional
        Column alignment specifier. The default is `None` and results in
        `'l'*N`, where `N` is the number of columns in data.
    header: list, None
        A list of str that are used as headers (separated from data with a
        horizontal line)

    Returns
    -------
    tex_string: str
        The resulting tex string of the table
    """
    return Template.table(data=data, cols=cols, header=header, **kwargs)

def make_section(title, newpage=False, starred=False):
    """ Creates a tex block for a section

    Parameters
    ----------
    title: str
        The title of the section
    newpage: bool, optional
        If `True` a newpage command is added *before* the section command.
        Default: False
    starred: bool, optional
        If `True`, the section is added with a star (*), such that it is not
        numbered in the resulting report. Default: False

    Returns
    -------
    tex_string: str
        The resulting tex string of the section element
    """
    return Template.section(sectiontype='section', sectiontitle=title,
            newpage=newpage, starred=starred)

def make_subsection(title, newpage=False, starred=False):
    """ Creates a tex block for a subsection

    Refer to documentation of `make_section`
    """
    return Template.section(sectiontype='subsection', sectiontitle=title,
            newpage=newpage, starred=starred)

def make_subsubsection(title, newpage=False, starred=False):
    """ Creates a tex block for a subsubsection

    Refer to documentation of `make_section`
    """
    return Template.section(sectiontype='subsubsection', sectiontitle=title,
            newpage=newpage, starred=starred)

def make_equation(content):
    return Template.equation.substitute(equation=content)



def make_figure(dimension_spec, size, fname, **kwargs):
    """ Creates a tex block for a figure.

    Parameters
    ----------
    dimension_spec: str
        defines the dimension of the figure that is specified: {'width',
        'height', 'widthratio', 'heightratio'}. The first two define absolute
        values, and the latter (ratio options) make definitions wrt to
        /textwidth and /textheight respectively.
    size: float 
        The actual size argument, that is added to the dimension_spec.
        --> dimension_spec=size.
    fname: str
        The filename of the figure that should be included
    """
    return Template.figure(dimension=dimension_spec, size=size, fname=fname,
            **kwargs)

class Report(object):
    """Class to generate a tex report. Writes to an open tex file. Has methods
    to conveniently add elements.

    """

    def __init__(self, fname, working_dir, pagesize='a4paper',
            orientation='portrait', fontsize=10, author='', title='',
            date=datetime.datetime.today(), left='2cm', right='2cm', top='2cm',
            bottom='2cm'):
        """ Constructor of Report
        
        Parameters
        ----------
        fname: str
            The filename of the resulting tex report. if the '.tex' ending is
            ommited, it is added automatically. This should only be the
            filename (no path).
        working_dir: str
            The path to the directory in which we want to operate. If this does
            not exist, it is created. We also create a subdirectory called
            'figures', which will be used to store plots / figures.
        papersize: str, optional
            The papersize of the doc. Has to be known by latex. Default:
            'a4paper'
        orientation: str, optional
            The page orientation {'portrait', 'landscape'}. Default: 'portrait'
        fontsize: int, optional
            The font size. Default: 10
        author: str, optional
            The author tag, Default: ''
        title: str, optional
            The title of the document. Default: ''
        date: datetime.datetime, optional:
            The date in the doc title. Default: datetime.datetime.today()
        left: str, optional
            The left margin. Default: '2cm'
        right: str, optional
            The right margin. Default: '2cm'
        top: str, optional
            The top margin. Default: '2cm'
        bottom: str, optional
            The bottom margin. Default: '2cm'
        """
        #prepare working dir(s):
        def safe_create_dir(path):
            if not os.path.exists(path):
                os.makedirs(path)
        self.working_dir = working_dir
        self.figure_dir = os.path.join(self.working_dir, 'figures')
        safe_create_dir(self.working_dir)
        safe_create_dir(self.figure_dir)

        if not fname.endswith('.tex'):
            fname += '.tex'
        self.fname = os.path.join(self.working_dir, fname)
        self.orientation = orientation
        self.pagesize = pagesize
        self.left = Length(left) 
        self.right = Length(right)
        self.top = Length(top) 
        self.bottom = Length(bottom)
        self.f = open(self.fname, 'w')
        self.f.write(Template.head.substitute(pagesize=pagesize,
            orientation=orientation, fontsize=fontsize, title=title,
            author=author, date=date.strftime('%d.%m.%Y'), left=left,
            right=right, top=top, bottom=bottom))
        self.force_all = False

    def get_textwidth_pt(self):
        """Get the textwidth of the doc in pt. 
        """
        left = self.left.get_value_in('pt')
        right = self.right.get_value_in('pt')
        if self.orientation == 'portrait':
            paper_witdh = Length(papersizes_wh_cm[self.pagesize][0],'cm')
        elif self.orientation == 'landsacpe':
            paper_witdh = Length(papersizes_wh_cm[self.pagesize][1],'cm')
        else:
            raise Exception('Unknown page orientation: %s' % self.orientation)
        return paper_witdh.get_value_in('pt') - left - right 

    def get_textheight_pt(self):
        """Get the textwidth of the doc in pt. 
        """
        top = self.top.get_value_in('pt')
        bottom = self.bottom.get_value_in('pt')
        if self.orientation == 'portrait':
            paper_height = Length(papersizes_wh_cm[self.pagesize][1],'cm')
        elif self.orientation == 'landsacpe':
            paper_height = Length(papersizes_wh_cm[self.pagesize][0],'cm')
        else:
            raise Exception('Unknown page orientation: %s' % self.orientation)
        return paper_height.get_value_in('pt') - top - bottom 

#    def add_preamble(self, preamble):
#        """ NOT IMPLEMENTED"""
#        raise NotImplemented('will do it at some point')
    
    def make_plot(self, fig, widthratio=None, heightratio=None, width=None,
            height=None, frmt='pdf', name=None, force=False, after_plotting=
            lambda: None, **kwargs):
        """ Dumps a matplotlib figure to disk and creates the corresponding tex
        block.

        This function saves the provided figure to the correct folder
        (working_dir/figures) and returns the corresponding tex block.

        If the name parameter is specified and force is False, the figure is
        only saved if the file does not exist. This gives sort of a caching
        functionality, especially in combination with defining a generator,
        which is then allows to only build the graph if required.

        Parameters
        ----------
        fig: a matplotlib.Figure or a callable 
            Either a matplotlib figure which we should save, or a function that
            returns one
        widthratio: float, optional
            The width of the figure as a ratio of textwidth. Default: None
        heightratio: float, optional
            The height of the figure as a ratio of textheight. Default: None
        width: float, optional
            The absolute width of the figure. Default: None
        height: float, optional
            The absolute height of the figure. Default: None
        frmt: str, optional
            The file format of the resulting figure. Default:'pdf'
        name: str, optional
            A name for the figure file. The default is None. If it is set to
            None, a random one is created.
        force: bool, optional
            If true, the figure is saved even if the file already exists.
            Default: False
        after_plotting: callable, optional
            A function which will be executed after plotting. This could for
            instance be used to close figures after plotting
        """
        # build the filename
        name = ''.join([rnd.choice(string.ascii_letters) for _ in range(30)]) \
                if name is None else name
        filename = os.path.join(self.figure_dir, name + '.' + frmt.strip(' .'))
        # check if and how we need to specify the size of the figure
        lornone = lambda x: None if x is None else Length(x)
        values = [widthratio, heightratio, lornone(width), lornone(height)]
        dims = ['width', 'height', 'width', 'height']
        factors = [lambda: Length(self.get_textwidth_pt(),'pt'), 
                lambda: Length(self.get_textheight_pt(),'pt')] + [lambda: 1]*2
        #make sure that we only have one specification
        temp = [x is not None for x in values]
        assert(sum(temp)==1), \
                "you have to provide exactly one size specification"
        idx = temp.index(True)
        methods = [r'{}', r'{}', r'{}', r'{}']
        # check if we need to save the plot
        if (not os.path.exists(filename)) or force or self.force_all:
            if hasattr(fig, '__call__'):
                fig = fig()
            print "writing plot:", filename
            fsize = [i.item() for i in fig.get_size_inches()]
            target = values[idx]*factors[idx]()
            target.dpi = 0.9*72.# fig.get_dpi() #slightly smaller to account
                                # for slightly heavier fonts compared to latex
            if dims[idx] == 'width':
                scale = target.convert_to('in').value / fsize[0]
            else:
                scale = target.convert_to('in').value / fsize[1]
            fig.set_size_inches(*[i*scale for i in fsize], forward=True)
            fig.gca().relim()
            fig.savefig(filename)
            after_plotting()

        return Template.figure(dimension=dims[idx],
                size=methods[idx].format(str(values[idx]*factors[idx]())),
                fname=filename,**kwargs)


    def add_plot(self, generator=lambda: None, widthratio=None,
            heightratio=None, width=None, height=None, fig=None, frmt='pdf',
            name=None, force=False, close_fig=False, **kwargs):
        """ Add a matplotlib plot to the report.

        This function wraps the 'make_plot' function and saves the result to
        the tex file.
            
        See documentation of make_plot for parameter descriptions.
        """
        self.f.write(self.make_plot(generator=generator, widthratio=widthratio,
            heightratio=heightratio, width=width, height=height, fig=fig,
            frmt=frmt, name=name, force=force, close_fig=close_fig, **kwargs))

    def add_equation(self, content):
        """Adds an equation to the report.
        
        Wraps make_equation.
        """
        self.f.write(make_equation(content=content))


    def add_table(self, data, cols=None, header=None, **kwargs):
        """Adds a table to the report.
        
        Wraps make_table.
        """
        self.f.write(make_table(data, cols=cols, header=header, **kwargs))


    def add_section(self, title, newpage=False, starred=False):
        """Adds a section to the report.
        
        Wraps make_section.
        """
        self.f.write(make_section(title=title, newpage=newpage, 
            starred=starred))

    def add_subsection(self, title, newpage=False, starred=False):
        """Adds a subsection to the report.
        
        Wraps make_subsection.
        """
        self.f.write(make_subsection(title=title, newpage=newpage, 
            starred=starred))

    def add_subsubsection(self, title, newpage=False, starred=False):
        """Adds a subsubsection to the report.
        
        Wraps make_subsubsection.
        """
        self.f.write(make_subsubsection(title=title, newpage=newpage, 
            starred=starred))

    def add_text(self, text):
        """ Add simple text to the document
        """
        self.f.write(text)
        self.f.write('\n')

    def add(self, stuff):
        """ Add variable things to the report. 

        Stuff is expected to be a string, or a list of strings. This is useful
        if tex blocks were created using a make_* function but not directly
        added to the report (as oposed to using add_* functions).
        """

        if type(stuff) is str:
            self.f.write(stuff)
            if not stuff.endswith('\n'):
                self.f.write('\n')
        else: #assume list of strings
            self.f.write('\n'.join(stuff))
            self.f.write('\n')


    def close(self, build=False):
        """ Finish the report and close the file

        Parameters
        ----------
        build: bool, optional
            If true, pdflatex is called to build the pdf from the tex file.
            Default: False
        """

        self.f.write(Template.tail)
        self.f.close()
        if build:
            os.system('cd %s; pdflatex %s' % (self.working_dir, self.fname))
    
def bold(s):
    """ Helper function to create bold tex text
    """
    return r' {{\bf {}}}'.format(s)

def italic(s):
    """ Helper function to create italic tex text
    """
    return r' {{\it {}}}'.format(s)


