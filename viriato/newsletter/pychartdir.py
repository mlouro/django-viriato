import sys, os, time, string

CDPYVersion = 0x500

ver = sys.version[:3]
if ver == "1.5" :
	import pychartdir15
	dll = pychartdir15
elif ver == "1.6" :
	import pychartdir16
	dll = pychartdir16
elif ver == "2.0" :
	import pychartdir20
	dll = pychartdir20
elif ver == "2.1" :
	import pychartdir21
	dll = pychartdir21
elif ver == "2.2" :
	import pychartdir22
	dll = pychartdir22
elif ver == "2.3" :
	import pychartdir23
	dll = pychartdir23
elif ver == "2.4" :
	import pychartdir24
	dll = pychartdir24
elif ver == "2.5" :
	import pychartdir25
	dll = pychartdir25
else :
	import pychartdir26
	dll = pychartdir26

#main DLL interface
_r = dll.callMethod

#version checking
dllVersion = (_r("getVersion") >> 16) & 0xffff
if dllVersion != CDPYVersion :
	raise ImportError('Version mismatch - "pychartdir.py" is of version %s.%s, but "chartdir.dll/libchartdir.so" is of version %s.%s' % ((CDPYVersion >> 8) & 0xff, CDPYVersion & 0xff, (dllVersion >> 8) & 0xff, dllVersion & 0xff))

def cdFindSubClass(classNames, c) :
	if classNames.has_key(c.__name__) :
		return c
	for s in c.__bases__ :
		ret = cdFindSubClass(classNames, s)
		if ret != None :
			return ret
	return None
	
def cdFindDefaultArgs(c, varName) :
	ret = c.__dict__.get("defaultArgs")
	if ret != None:
		ret = ret.get(varName)
		if ret != None:
			return ret
	for s in c.__bases__ :
		ret = cdFindDefaultArgs(s, varName)
		if ret != None :
			return ret
	return None	

#utility to call DLL method
class MethodWrapper :
	def __init__(self, obj, id) :
		self.obj = obj
		self.id = id
	def __call__(self, *args) :
		classObj = cdFindSubClass(globals(), self.obj.__class__)
		if classObj == None :
			classObj = self.obj.__class__
		defaultArgs = cdFindDefaultArgs(classObj, self.id)
		if defaultArgs != None and len(defaultArgs) > 1 :
			if len(args) < defaultArgs[1] - len(defaultArgs) + 2 :
				raise TypeError("Wrong number of arguments; expecting at least %d but received %d" %(defaultArgs[1] - len(defaultArgs) + 2, len(args)))
			if len(args) < defaultArgs[1] :
				args = args + defaultArgs[len(defaultArgs) - defaultArgs[1] + len(args):]
		ret = apply(_r, (classObj.__name__ + "." + self.id, self.obj.this) + args)
		if defaultArgs != None and len(defaultArgs) > 0 and defaultArgs[0] != None :
			return defaultArgs[0](ret)
		else :
			return ret

class AutoMethod :
	def __init__(self, this) :
		self.this = this
	def __getattr__(self, name) :
		if name[:2] == "__" :
			raise AttributeError 
		return MethodWrapper(self, name)

def argIsArray(a) :
	return type(a) == type([]) or type(a) == type(())
	
def encodeIfArray(b, a) :
	if argIsArray(a) : 
		return b + "2" 
	return b

def decodePtr(p) :
	if p is None :
		return '$$pointer$$null'
	if hasattr(p, "this") :
		return p.this
	else :
		return p
		
#///////////////////////////////////////////////////////////////////////////////////
#//	constants
#///////////////////////////////////////////////////////////////////////////////////

BottomLeft = 1
BottomCenter = 2
BottomRight = 3	
Left = 4
Center = 5
Right = 6
TopLeft = 7
TopCenter = 8
TopRight = 9
Top = TopCenter
Bottom = BottomCenter
TopLeft2 = 10
TopRight2 = 11
BottomLeft2 = 12
BottomRight2 = 13
	
Transparent = 0xff000000L
Palette = 0xffff0000L
BackgroundColor = 0xffff0000L 
LineColor = 0xffff0001L
TextColor = 0xffff0002L
DataColor = 0xffff0008L
SameAsMainColor = 0xffff0007L

HLOCDefault = 0
HLOCOpenClose = 1
HLOCUpDown = 2

DiamondPointer = 0
TriangularPointer = 1
ArrowPointer = 2
ArrowPointer2 = 3
LinePointer = 4
PencilPointer = 5

SmoothShading = 0
TriangularShading = 1
RectangularShading = 2
TriangularFrame = 3
RectangularFrame = 4
	
ChartBackZ = 0x100
ChartFrontZ = 0xffff
PlotAreaZ = 0x1000
GridLinesZ = 0x2000

XAxisSymmetric = 1
XAxisSymmetricIfNeeded = 2
YAxisSymmetric = 4
YAxisSymmetricIfNeeded = 8
XYAxisSymmetric = 16
XYAxisSymmetricIfNeeded = 32

XAxisAtOrigin = 1
YAxisAtOrigin = 2
XYAxisAtOrigin = 3
	
NoValue = 1.7e308
LogTick = 1.6e308
LinearTick = 1.5e308
TickInc = 1.0e200
MinorTickOnly = -1.7e308
MicroTickOnly = -1.6e308
TouchBar = -1.7e-100
AutoGrid = -2

NoAntiAlias = 0
AntiAlias = 1
AutoAntiAlias = 2

TryPalette = 0
ForcePalette = 1
NoPalette = 2
Quantize = 0
OrderedDither = 1
ErrorDiffusion = 2

BoxFilter = 0
LinearFilter = 1
QuadraticFilter = 2
BSplineFilter = 3
HermiteFilter = 4
CatromFilter = 5
MitchellFilter = 6
SincFilter = 7
LanczosFilter = 8
GaussianFilter = 9
HanningFilter = 10
HammingFilter = 11
BlackmanFilter = 12
BesselFilter = 13

PNG = 0
GIF = 1
JPG = 2
WMP = 3
BMP = 4
SVG = 5
SVGZ = 6

Overlay = 0
Stack = 1
Depth = 2
Side = 3
Percentage = 4
	
defaultPalette = [
	0xffffff, 0x000000, 0x000000, 0x808080, 
	0x808080, 0x808080, 0x808080, 0x808080,
	0xff3333, 0x33ff33, 0x6666ff, 0xffff00, 
	0xff66ff, 0x99ffff,	0xffcc33, 0xcccccc, 
	0xcc9999, 0x339966, 0x999900, 0xcc3300,	
	0x669999, 0x993333, 0x006600, 0x990099,
	0xff9966, 0x99ff99, 0x9999ff, 0xcc6600,
	0x33cc33, 0xcc99ff, 0xff6666, 0x99cc66,
	0x009999, 0xcc3333, 0x9933ff, 0xff0000,
	0x0000ff, 0x00ff00, 0xffcc99, 0x999999,
	-1
]

whiteOnBlackPalette = [
	0x000000, 0xffffff, 0xffffff, 0x808080, 
	0x808080, 0x808080, 0x808080, 0x808080,
	0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 
	0xff00ff, 0x66ffff,	0xffcc33, 0xcccccc, 
	0x9966ff, 0x339966, 0x999900, 0xcc3300,	
	0x99cccc, 0x006600, 0x660066, 0xcc9999,
	0xff9966, 0x99ff99, 0x9999ff, 0xcc6600,
	0x33cc33, 0xcc99ff, 0xff6666, 0x99cc66,
	0x009999, 0xcc3333, 0x9933ff, 0xff0000,
	0x0000ff, 0x00ff00, 0xffcc99, 0x999999,
	-1
]

transparentPalette = [ 
	0xffffff, 0x000000, 0x000000, 0x808080, 
	0x808080, 0x808080, 0x808080, 0x808080,
	0x80ff0000L, 0x8000ff00L, 0x800000ffL, 0x80ffff00L, 
	0x80ff00ffL, 0x8066ffffL, 0x80ffcc33L, 0x80ccccccL, 
	0x809966ffL, 0x80339966L, 0x80999900L, 0x80cc3300L,
	0x8099ccccL, 0x80006600L, 0x80660066L, 0x80cc9999L,
	0x80ff9966L, 0x8099ff99L, 0x809999ffL, 0x80cc6600L,
	0x8033cc33L, 0x80cc99ffL, 0x80ff6666L, 0x8099cc66L,
	0x80009999L, 0x80cc3333L, 0x809933ffL, 0x80ff0000L,
	0x800000ffL, 0x8000ff00L, 0x80ffcc99L, 0x80999999L,
	-1
]

NoSymbol = 0
SquareSymbol = 1
DiamondSymbol = 2
TriangleSymbol = 3
RightTriangleSymbol = 4
LeftTriangleSymbol = 5
InvertedTriangleSymbol = 6
CircleSymbol = 7
CrossSymbol = 8
Cross2Symbol = 9
PolygonSymbol = 11
Polygon2Symbol = 12
StarSymbol = 13
CustomSymbol = 14 
	
NoShape = 0
SquareShape = 1
DiamondShape = 2
TriangleShape = 3
RightTriangleShape = 4
LeftTriangleShape = 5
InvertedTriangleShape = 6
CircleShape = 7
CircleShapeNoShading = 10
GlassSphereShape = 15
GlassSphere2Shape = 16
SolidSphereShape = 17

def cdBound(a, b, c) :
	if b < a :
		return a
	if b > c :
		return c
	return b
	
def CrossShape(width = 0.5) :
	return CrossSymbol | (int(cdBound(0, width, 1) * 4095 + 0.5) << 12)
def Cross2Shape(width = 0.5) :
	return Cross2Symbol | (int(cdBound(0, width, 1) * 4095 + 0.5) << 12)
def PolygonShape(side) :
	return PolygonSymbol | (cdBound(0, side, 100) << 12)
def Polygon2Shape(side) :
	return Polygon2Symbol | (cdBound(0, side, 100) << 12)
def StarShape(side) :
	return StarSymbol | (cdBound(0, side, 100) << 12)

DashLine = 0x0505
DotLine = 0x0202
DotDashLine = 0x05050205
AltDashLine = 0x0A050505

goldGradient = [0, 0xFFE743, 0x60, 0xFFFFE0, 0xB0, 0xFFF0B0, 0x100, 0xFFE743]
silverGradient = [0, 0xC8C8C8, 0x60, 0xF8F8F8, 0xB0, 0xE0E0E0, 0x100, 0xC8C8C8]
redMetalGradient = [0, 0xE09898, 0x60, 0xFFF0F0, 0xB0, 0xF0D8D8, 0x100, 0xE09898]
blueMetalGradient = [0, 0x9898E0, 0x60, 0xF0F0FF, 0xB0, 0xD8D8F0, 0x100, 0x9898E0]
greenMetalGradient = [0, 0x98E098, 0x60, 0xF0FFF0, 0xB0, 0xD8F0D8, 0x100, 0x98E098]

def metalColor(c, angle = 90) :
	return _r("metalColor", c, angle)
def goldColor(angle = 90) :
	return metalColor(0xffee44, angle)
def silverColor(angle = 90) :
	return metalColor(0xdddddd, angle)
def brushedMetalColor(c, texture = 2, angle = 90) :
	return metalColor(c, angle) | ((texture & 0x3) << 18)
def brushedSilverColor(texture = 2, angle = 90) :
	return brushedMetalColor(0xdddddd, texture, angle)
def brushedGoldColor(texture = 2, angle = 90) :
	return brushedMetalColor(0xffee44, texture, angle)

SideLayout = 0
CircleLayout = 1

DefaultShading = 0
FlatShading = 1
LocalGradientShading = 2
GlobalGradientShading = 3
ConcaveShading = 4
RoundedEdgeNoGlareShading = 5
RoundedEdgeShading = 6
RadialShading = 7
RingShading = 8

NormalLegend = 0
ReverseLegend = 1
NoLegend = 2

PixelScale = 0
XAxisScale = 1
YAxisScale = 2
EndPoints = 3
AngularAxisScale = XAxisScale
RadialAxisScale = YAxisScale

MonotonicNone = 0 
MonotonicX = 1
MonotonicY = 2
MonotonicXY = 3
MonotonicAuto = 4

ConstrainedLinearRegression = 0
LinearRegression = 1
ExponentialRegression = -1
LogarithmicRegression = -2

def PolynomialRegression(n) :
	return n

StartOfHourFilterTag = 1
StartOfDayFilterTag = 2
StartOfWeekFilterTag = 3
StartOfMonthFilterTag = 4
StartOfYearFilterTag = 5
RegularSpacingFilterTag = 6
AllPassFilterTag = 7
NonePassFilterTag = 8
SelectItemFilterTag = 9

def StartOfHourFilter(labelStep = 1, initialMargin = 0.05) :
	return _r("encodeFilter", StartOfHourFilterTag, labelStep, initialMargin)
def StartOfDayFilter(labelStep = 1, initialMargin = 0.05) :
	return _r("encodeFilter", StartOfDayFilterTag, labelStep, initialMargin)
def StartOfWeekFilter(labelStep = 1, initialMargin = 0.05) :
	return _r("encodeFilter", StartOfWeekFilterTag, labelStep, initialMargin)
def StartOfMonthFilter(labelStep = 1, initialMargin = 0.05) :
	return _r("encodeFilter", StartOfMonthFilterTag, labelStep, initialMargin)
def StartOfYearFilter(labelStep = 1, initialMargin = 0.05) :
	return _r("encodeFilter", StartOfYearFilterTag, labelStep, initialMargin)
def RegularSpacingFilter(labelStep = 1, initialMargin = 0) :
	return _r("encodeFilter", RegularSpacingFilterTag, labelStep, initialMargin / 4095.0)
def AllPassFilter() :
	return _r("encodeFilter", AllPassFilterTag, 0, 0)
def NonePassFilter() :
	return _r("encodeFilter", NonePassFilterTag, 0, 0)
def SelectItemFilter(item) :
	return _r("encodeFilter", SelectItemFilterTag, item, 0)
	
NormalGlare = 3
ReducedGlare = 2
NoGlare	= 1

def glassEffect(glareSize = NormalGlare, glareDirection = Top, raisedEffect = 5) :
	return _r("glassEffect", glareSize, glareDirection, raisedEffect)
def softLighting(direction = Top, raisedEffect = 4) :
	return _r("softLighting", direction, raisedEffect)
def barLighting(startBrightness = 0.75, endBrightness = 1.5) :
	return _r("barLighting", startBrightness, endBrightness)
def cylinderEffect(orientation = Center, ambientIntensity = 0.5, diffuseIntensity = 0.5, specularIntensity = 0.75, shininess = 8) :
	return _r("cylinderEffect", orientation, ambientIntensity, diffuseIntensity, specularIntensity, shininess)

AggregateSum = 0
AggregateAvg = 1
AggregateStdDev = 2
AggregateMin = 3
AggregateMed = 4
AggregateMax = 5
AggregatePercentile = 6
AggregateFirst = 7
AggregateLast = 8
AggregateCount = 9
		
#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to libgraphics.h
#///////////////////////////////////////////////////////////////////////////////////
class TTFText(AutoMethod) :
	#obsoleted constants - for compatibility only
	NoAntiAlias = 0
	AntiAlias = 1
	AutoAntiAlias = 2

	defaultArgs = {
		"draw":(None, 4, TopLeft)
	}
		
	def __init__(self, this, parent) :
		self.this = this
		self.parent = parent
	def __del__(self) :
		_r("TTFText.destroy", self.this)

class DrawArea(AutoMethod) :
	#obsoleted constants - for compatibility only
	TryPalette = 0
	ForcePalette = 1
	NoPalette = 2
	Quantize = 0
	OrderedDither = 1
	ErrorDiffusion = 2

	defaultArgs = {
		"setSize":(None, 3, 0xffffff),
		"resize":(None, 4, LinearFilter, 1),
		"move":(None, 5, 0xffffff, LinearFilter, 1),
		"rotate":(None, 6, 0xffffff, -1, -1, LinearFilter, 1),
		"line":(None, 6, 1),
		"rect":(None, 7, 0),
		"text2":(None, 11, TopLeft),
		"rAffineTransform":(None, 9, 0xffffff, LinearFilter, 1),
		"affineTransform":(None, 9, 0xffffff, LinearFilter, 1),
		"sphereTransform":(None, 5, 0xffffff, LinearFilter, 1),
		"hCylinderTransform":(None, 4, 0xffffff, LinearFilter, 1),
		"vCylinderTransform":(None, 4, 0xffffff, LinearFilter, 1),
		"vTriangleTransform":(None, 4, -1, 0xffffff, LinearFilter, 1),
		"hTriangleTransform":(None, 4, -1, 0xffffff, LinearFilter, 1),
		"shearTransform":(None, 5, 0, 0xffffff, LinearFilter, 1),
		"waveTransform":(None, 8, 0, 0, 0, 0xffffff, LinearFilter, 1),
		"outJPG":(None, 2, 80),
		"outSVG":(None, 2, ""),
		"outJPG2":(None, 1, 80),
		"outSVG2":(None, 1, ""),
		"setAntiAlias":(None, 2, 1, AutoAntiAlias),
		"dashLineColor":(None, 2, DashLine),
		"patternColor2":(None, 3, 0, 0),
		"gradientColor2":(None, 5, 90, 1, 0, 0),
		"setDefaultFonts":(None, 4, "", "", ""),
		"reduceColors":(None, 2, 0),
		"linearGradientColor":(None, 7, 0),
		"linearGradientColor2":(None, 6, 0),
		"radialGradientColor":(None, 7, 0),
		"radialGradientColor2":(None, 6, 0)
		}
	def __init__(self, this = None) :
		if this == None :
			self.own_this = 1
			self.this = _r("DrawArea.create")
		else :
			self.own_this = 0
			self.this = this
	def __del__(self) :
		if self.own_this and self.this != None :
			_r("DrawArea.destroy", self.this)
	def clone(self, d, x, y, align, newWidth = -1, newHeight = -1, ft = LinearFilter, blur = 1) :
		_r("DrawArea.clone", self.this, d.this, x, y, align, newWidth, newHeight, ft, blur)
	def polygon(self, points, edgeColor, fillColor) :
		_r("DrawArea.polygon", self.this, 
			map(lambda a: a[0], points), map(lambda a: a[1], points), edgeColor, fillColor)
	def fill(self, x, y, color, borderColor = None) :
		if borderColor == None :
			_r("DrawArea.fill", self.this, x, y, color)
		else :
			self.fill2(x, y, color, borderColor)
	def text3(self, str, font, fontSize) :
		return TTFText(_r("DrawArea.text3", self.this, str, font, fontSize), self)
	def text4(self, text, font, fontIndex, fontHeight, fontWidth, angle, vertical) :
		return TTFText(_r("DrawArea.text4", self.this, text, font, fontIndex, fontHeight, fontWidth, angle, vertical), self)
	def merge(self, d, x, y, align, transparency) :
		_r("DrawArea.merge", self.this, d.this, x, y, align, transparency)
	def tile(self, d, transparency) :
		_r("DrawArea.tile", self.this, d.this, transparency)
	def patternColor(self, c, h = None, startX = 0, startY = 0) :
		if h == None :
			return self.patternColor2(c)
		else :
			return _r("DrawArea.patternColor", self.this, c, h, startX, startY)
	def gradientColor(self, startX, startY = 90, endX = 1, endY = 0, startColor = 0, endColor = None) :
		if endColor == None :
			return self.gradientColor2(startX, startY, endX, endY, startColor)
		else :
			return _r("DrawArea.gradientColor", self.this, startX, startY, endX, endY, startColor, endColor)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to drawobj.h
#///////////////////////////////////////////////////////////////////////////////////
class Box(AutoMethod) :
	defaultArgs = {
		"setBackground":(None, 3, -1, 0),
		"getImageCoor":(None, 2, 0, 0),
		"setRoundedCorners":(None, 4, 10, -1, -1, -1)
	}

class TextBox(Box) :
	defaultArgs = {
		"setFontStyle":(None, 2, 0),
		"setFontSize":(None, 2, 0),
		"setFontAngle":(None, 2, 0),
		"setTruncate":(None, 2, 1) 
	}
	
class Line(AutoMethod) : 
	pass
	
class CDMLTable(AutoMethod) :
	defaultArgs = {
		"setPos":(None, 3, TopLeft),
		"insertCol":(TextBox, 1),
		"appendCol":(TextBox, 0),
		"insertRow":(TextBox, 1),
		"appendRow":(TextBox, 0),
		"setText":(TextBox, 3),
		"setCell":(TextBox, 5),
		"getCell":(TextBox, 2),
		"getColStyle":(TextBox, 1),
		"getRowStyle":(TextBox, 1),
		"getStyle":(TextBox, 0),
	}

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to basechart.h
#///////////////////////////////////////////////////////////////////////////////////
class LegendBox(TextBox) :
	defaultArgs = {
		"setKeySize":(None, 3, -1, -1),
		"setKeySpacing":(None, 2, -1),
		"setKeyBorder":(None, 2, 0),
		"setReverse":(None, 1, 1),
		"setLineStyleKey":(None, 1, 1),
		"getHTMLImageMap":(None, 5, "", "", 0, 0)		
	}
	def addKey(self, text, color, lineWidth = 0, drawarea = None) :
		_r("LegendBox.addKey", self.this, text, color, lineWidth, decodePtr(drawarea))
	def	addKey2(self, pos, text, color, lineWidth = 0, drawarea = None) :
		_r("LegendBox.addKey2", self.this, pos, text, color, lineWidth, decodePtr(drawarea))
	def getImageCoor2(self, dataItem, offsetX = 0, offsetY = 0) :
		return _r("LegendBox.getImageCoor", self.this, dataItem, offsetX, offsetY)

class BaseChart(AutoMethod) :
	#obsoleted constants - for compatibility only
	PNG = 0
	GIF = 1
	JPG = 2
	WMP = 3

	defaultArgs = {
		"setBackground":(None, 3, -1, 0),
		"setBgImage":(None, 2, Center),
		"setDropShadow":(None, 4, 0xaaaaaa, 5, 0x7fffffff, 5),
		"setAntiAlias":(None, 2, 1, AutoAntiAlias),
		"addTitle2":(TextBox, 7, "", 12, TextColor, Transparent, Transparent),
		"addTitle":(TextBox, 6, "", 12, TextColor, Transparent, Transparent),
		"addLegend":(LegendBox, 5, 1, "", 10),
		"addLegend2":(LegendBox, 5, 1, "", 10),
		"getLegend":(LegendBox, 0),
		"layoutLegend":(LegendBox, 0),
		"getDrawArea":(DrawArea, 0),
		"addText":(TextBox, 9, "", 8, TextColor, TopLeft, 0, 0),
		"addLine":(Line, 6, LineColor, 1),
		"addTable":(CDMLTable, 5),
		"dashLineColor":(None, 2, DashLine),
		"patternColor2":(None, 3, 0, 0),
		"gradientColor2":(None, 5, 90, 1, 0, 0),
		"setDefaultFonts":(None, 4, "", "", ""),
		"setNumberFormat":(None, 3, "~", ".", "-"),
		"makeChart3":(DrawArea, 0),
		"getHTMLImageMap":(None, 5, "", "", 0, 0),
		"setRoundedFrame":(None, 5, 0xffffff, 10, -1, -1, -1),
		"linearGradientColor":(None, 7, 0),
		"linearGradientColor2":(None, 6, 0),
		"radialGradientColor":(None, 7, 0),
		"radialGradientColor2":(None, 6, 0),
		}
	this = None
	def __del__(self) :
		if self.this != None :
			_r("BaseChart.destroy", self.this)
	def addDrawObj(self, obj) :
		_r("BaseChart.addDrawObj", obj.this)
		return obj
	def patternColor(self, c, h = None, startX = 0, startY = 0) :
		if h == None :
			return self.patternColor2(c)
		else :
			return _r("BaseChart.patternColor", self.this, c, h, startX, startY)
	def gradientColor(self, startX, startY = 90, endX = 1, endY = 0, startColor = 0, endColor = None) :
		if endColor == None :
			return self.gradientColor2(startX, startY, endX, endY, startColor)
		else :
			return _r("BaseChart.gradientColor", self.this, startX, startY, endX, endY, startColor, endColor)
	def makeTmpFile(self, path, imageFormat = PNG, lifeTime = 600) :
		path = normalizePath(path)
		filename = tmpFile2(path, lifeTime, "." + {JPG:"jpg", GIF:"gif", BMP:"bmp", WMP:"wbmp", SVG:"svg", SVGZ:"svgz"}.get(imageFormat, "png"))
		if self.makeChart(path + "/" + filename) :
			return filename
		else :
			return ""		

class MultiChart(BaseChart) :
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("MultiChart.create", width, height, bgColor, edgeColor, raisedEffect)
		self.dependencies = []
	def addChart(self, x, y, c) :
		_r("MultiChart.addChart", self.this, x, y, c.this)
		self.dependencies.append(c)
	def setMainChart(self, c) :
		_r("MultiChart.setMainChart", self.this, c.this)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to piechart.h
#///////////////////////////////////////////////////////////////////////////////////
class Sector(AutoMethod) :
	defaultArgs = {
		"setExplode":(None, 1, -1),
		"setLabelStyle":(TextBox, 3, "", 8, TextColor),
		"setLabelPos":(None, 2, -1),
		"setLabelLayout":(None, 2, -1),
		"setJoinLine":(None, 2, 1),
		"setColor":(None, 3, -1, -1),
		"setStyle":(None, 3, -1, -1),
		"getImageCoor":(None, 2, 0, 0),
		"getLabelCoor":(None, 2, 0, 0)
		}
	
class PieChart(BaseChart) :
	defaultArgs = {
		"setStartAngle":(None, 2, 1),
		"setExplode":(None, 2, -1, -1),
		"setExplodeGroup":(None, 3, -1),
		"setLabelStyle":(TextBox, 3, "", 8, TextColor),
		"setLabelPos":(None, 2, -1),
		"setLabelLayout":(None, 4, -1, -1, -1),
		"setJoinLine":(None, 2, 1),
		"setLineColor":(None, 2, -1),
		"setSectorStyle":(None, 3, -1, -1),
		"setData":(None, 2, None),
		"sector":(Sector, 1),
		"set3D2":(None, 3, -1, 0)
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("PieChart.create", width, height, bgColor, edgeColor, raisedEffect)
	def set3D(self, depth = -1, angle = -1, shadowMode = 0) :
		_r(encodeIfArray("PieChart.set3D", depth), self.this, depth, angle, shadowMode)
	def getSector(self, sectorNo) :
		return self.sector(sectorNo)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to axis.h
#///////////////////////////////////////////////////////////////////////////////////
class Mark(TextBox) :
	def setMarkColor(self, lineColor, textColor = -1, tickColor = -1) :
		_r("Mark.setMarkColor", self.this, lineColor, textColor, tickColor)
	
class Axis(AutoMethod) :
	defaultArgs = {
		"setLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"setTitle":(TextBox, 4, "", 8, TextColor),
		"setTitlePos":(None, 2, 3),
		"setColors":(None, 4, TextColor, -1, -1),
		"setTickWidth":(None, 2, -1),
		"setTickColor":(None, 2, -1),
		"setMargin":(None, 2, 0),
		"setAutoScale":(None, 3, 0.1, 0.1, 0.8),
		"setTickDensity":(None, 2, -1),
		"setReverse":(None, 1, 1),
		"setLabels2":(TextBox, 2, ""),
		"makeLabelTable":(CDMLTable, 0),
		"getLabelTable":(CDMLTable, 0),
		"setLinearScale3":(None, 1, ""),
		"setDateScale3":(None, 1, ""),
		"addMark":(Mark, 5, "", "", 8),
		"addLabel2":(None, 3, 0),
		"getAxisImageMap":(None, 7, "", "", 0, 0),
		"getHTMLImageMap":(None, 5, "", "", 0, 0),
		"setMultiFormat2":(None, 4, 1, 1),
		"setLabelStep":(None, 4, 0, 0, -0x7fffffff),
		"setFormatCondition":(None, 2, 0)
		}
	def setTickLength(self, majorTickLen, minorTickLen = None) :
		if minorTickLen == None :
			_r("Axis.setTickLength", self.this, majorTickLen)
		else :
			self.setTickLength2(majorTickLen, minorTickLen)
	def setTopMargin(self, topMargin) :
		self.setMargin(topMargin)
	def setLabels(self, labels, formatString = None) :
		if formatString == None :
			return TextBox(_r("Axis.setLabels", self.this, labels))
		else :
			return self.setLabels2(labels, formatString)
	def setLinearScale(self, lowerLimit = None, upperLimit = None, majorTickInc = 0, minorTickInc = 0) :
		if lowerLimit == None :
			self.setLinearScale3()
		elif upperLimit == None :
			self.setLinearScale3(lowerLimit)
		elif argIsArray(majorTickInc) :
			self.setLinearScale2(lowerLimit, upperLimit, majorTickInc)
		else :
			_r("Axis.setLinearScale", self.this, lowerLimit, upperLimit, majorTickInc, minorTickInc)
	def setLogScale(self, lowerLimit = None, upperLimit = None, majorTickInc = 0, minorTickInc = 0) :
		if lowerLimit == None :
			self.setLogScale3()
		elif upperLimit == None :
			self.setLogScale3(lowerLimit)
		elif argIsArray(majorTickInc) :
			self.setLogScale2(lowerLimit, upperLimit, majorTickInc)
		else :
			_r("Axis.setLogScale", self.this, lowerLimit, upperLimit, majorTickInc, minorTickInc)
	def setLogScale2(self, lowerLimit, upperLimit, labels = 0) :
		if argIsArray(labels) :
			_r("Axis.setLogScale2", self.this, lowerLimit, upperLimit, labels)
		else :
			#compatibility with ChartDirector Ver 2.5
			self.setLogScale(lowerLimit, upperLimit, labels)
	def setLogScale3(self, formatString = "") :
		if type(formatString) != type("") :
			#compatibility with ChartDirector Ver 2.5
			if formatString :
				self.setLogScale3()
			else :
				self.setLinearScale3()
		else :
			_r("Axis.setLogScale3", self.this, formatString)
	def setDateScale(self, lowerLimit = None, upperLimit = None, majorTickInc = 0, minorTickInc = 0) :
		if lowerLimit == None :
			self.setDateScale3()
		elif upperLimit == None :
			self.setDateScale3(lowerLimit)
		elif argIsArray(majorTickInc) :
			self.setDateScale2(lowerLimit, upperLimit, majorTickInc)
		else :
			_r("Axis.setDateScale", self.this, lowerLimit, upperLimit, majorTickInc, minorTickInc)
	def syncAxis(self, axis, slope = 1, intercept = 0) :
		_r("Axis.syncAxis", self.this, axis.this, slope, intercept)
	def copyAxis(self, axis) :
		_r("Axis.copyAxis", self.this, axis.this)
	def setMultiFormat(self, filter1, format1, filter2 = 1, format2 = None, labelSpan = 1, promoteFirst = 1) :
		if format2 == None :
			self.setMultiFormat2(filter1, format1, filter2, 1)
		else :
			_r("Axis.setMultiFormat", self.this, filter1, format1, filter2, format2, labelSpan, promoteFirst)

class ColorAxis(Axis) :
	defaultArgs = {
		"setColorGradient":(None, 4, 1, None, -1, -1),
		"setCompactAxis":(None, 1, 1),
		"setAxisBorder":(None, 2, 0),
		"setBoundingBox":(None, 3, Transparent, 0),
		"setRoundedCorners":(None, 4, 10, -1, -1, -1)
	}

class AngularAxis(AutoMethod) :
	defaultArgs = {
		"setLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"setReverse":(None, 1, 1),
		"setLabels2":(TextBox, 2, ""),
		"addZone2":(None, 4, -1),
		"getAxisImageMap":(None, 7, "", "", 0, 0),
		"getHTMLImageMap":(None, 5, "", "", 0, 0)
		}
	def setLabels(self, labels, formatString = None) :
		if formatString == None :
			return TextBox(_r("AngularAxis.setLabels", self.this, labels))
		else :
			return self.setLabels2(labels, formatString)
	def setLinearScale(self, lowerLimit, upperLimit, majorTickInc = 0, minorTickInc = 0) :
		if argIsArray(majorTickInc) :
			self.setLinearScale2(lowerLimit, upperLimit, majorTickInc)
		else :
			_r("AngularAxis.setLinearScale", self.this, lowerLimit, upperLimit, majorTickInc, minorTickInc)
	def addZone(self, startValue, endValue, startRadius, endRadius = -1, fillColor = None, edgeColor = -1) :
		if fillColor == None:
			self.addZone2(startValue, endValue, startRadius, endRadius)
		else :
			_r("AngularAxis.addZone", self.this, startValue, endValue, startRadius, endRadius, fillColor, edgeColor)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to layer.h
#///////////////////////////////////////////////////////////////////////////////////
class DataSet(AutoMethod) :
	defaultArgs = {
		"setDataColor":(None, 4, -1, -1, -1, -1),
		"setUseYAxis2":(None, 1, 1),
		"setDataLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"setDataSymbol4":(None, 4, 11, -1, -1)
		}
	def setDataSymbol(self, symbol, size = None, fillColor = -1, edgeColor = -1, lineWidth = 1) :
		if argIsArray(symbol) :
			if size == None :
				size = 11
			self.setDataSymbol4(symbol, size, fillColor, edgeColor)
			return
		if size == None :
			try :
				symbol = int(symbol)
				size = 5
			except :
				self.setDataSymbol2(symbol)
				return
		_r("DataSet.setDataSymbol", self.this, symbol, size, fillColor, edgeColor, lineWidth)
	def setDataSymbol2(self, image) :
		if hasattr(image, "this") :
			self.setDataSymbol3(image)
		else :
			_r("DataSet.setDataSymbol2", self.this, image)
	def setDataSymbol3(self, image) :
		_r("DataSet.setDataSymbol3", self.this, image.this)
	def setUseYAxis(self, yAxis) :
		_r("DataSet.setUseYAxis", self.this, yAxis.this)

class Layer(AutoMethod) :
	#obsoleted constants - for compatibility only
	Overlay = 0
	Stack = 1
	Depth = 2
	Side = 3

	defaultArgs = {
		"setBorderColor":(None, 2, 0),
		"set3D":(None, 2, -1, 0),
		"addDataSet":(DataSet, 3, -1, ""),
		"addDataGroup":(None, 1, ""),
		"getDataSet":(DataSet, 1),
		"setUseYAxis2":(None, 1, 1),
		"setLegendOrder":(None, 2, -1),
		"setDataLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"setAggregateLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"addCustomDataLabel":(TextBox, 7, "", 8, TextColor, 0),
		"addCustomAggregateLabel":(TextBox, 6, "", 8, TextColor, 0),
		"addCustomGroupLabel":(TextBox, 7, "", 8, TextColor, 0),
		"getImageCoor2":(None, 3, 0, 0),
		"getHTMLImageMap":(None, 5, "", "", 0, 0),
		"setHTMLImageMap":(None, 3, "", "")
		}
	def getImageCoor(self, dataSet, dataItem = None, offsetX = 0, offsetY = 0) :
		if dataItem == None :
			return self.getImageCoor2(dataItem)
		else :
			return _r("Layer.getImageCoor", self.this, dataSet, dataItem, offsetX, offsetY)
	def setXData(self, xData, dummy = None) :
		if dummy != None :
			self.setXData2(xData, dummy)
		else :
			_r("Layer.setXData", self.this, xData)
	def getYCoor(self, value, yAxis = 1) :
		if hasattr(yAxis, "this") :
			return _r("Layer.getYCoor2", self.this, value, yAxis.this)
		else :
			return _r("Layer.getYCoor", self.this, value, yAxis)
	def setUseYAxis(self, yAxis) :
		_r("Layer.setUseYAxis", self.this, yAxis.this)
	def yZoneColor(self, threshold, belowColor, aboveColor, yAxis = 1) :
		if hasattr(yAxis, "this") :
			return _r("Layer.yZoneColor2", self.this, threshold, belowColor, aboveColor, yAxis.this)
		else :
			return _r("Layer.yZoneColor", self.this, threshold, belowColor, aboveColor, yAxis)
	def alignLayer(self, layer, dataSet) :
		_r("Layer.alignLayer", self.this, layer.this, dataSet)
	def moveFront(self, layer = None) :
		_r("Layer.moveFront", self.this, decodePtr(layer))
	def moveBack(self, layer = None) :
		_r("Layer.moveFront", self.this, decodePtr(layer))

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to barlayer.h
#///////////////////////////////////////////////////////////////////////////////////
class BarLayer(Layer) :
	defaultArgs = {
		"setBarGap":(None, 2, 0.2),
		"setBarWidth":(None, 2, -1),
		"setIconSize":(None, 2, -1),
		"setOverlapRatio":(None, 2, 1),
		"setBarShape2":(None, 3, -1, -1)
	}
	def setBarShape(self, shape, dataGroup = -1, dataItem = -1) :
		_r(encodeIfArray("BarLayer.setBarShape", shape), self.this, shape, dataGroup, dataItem)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to linelayer.h
#///////////////////////////////////////////////////////////////////////////////////
class LineLayer(Layer) :
	defaultArgs = {
		"setGapColor":(None, 2, -1),
		"setSymbolScale":(None, 4, PixelScale, None, PixelScale),
		"getLine":(None, 1, 0)
	}
	
class ScatterLayer(LineLayer) :
	pass

class InterLineLayer(LineLayer) :
	def setGapColor(self, gapColor12, gapColor21 = -1) :
		_r("InterLineLayer.setGapColor", self.this, gapColor12, gapColor21)
	
class SplineLayer(LineLayer) :
	pass
		
class StepLineLayer(LineLayer) :
	pass
		
#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to arealayer.h
#///////////////////////////////////////////////////////////////////////////////////
class AreaLayer(Layer) :
	pass

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to trendlayer.h
#///////////////////////////////////////////////////////////////////////////////////
class TrendLayer(Layer) :
	defaultArgs = {
		"addConfidenceBand":(None, 7, Transparent, 1, -1, -1, -1),
		"addPredictionBand":(None, 7, Transparent, 1, -1, -1, -1),
	}
			
#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to hloclayer.h
#///////////////////////////////////////////////////////////////////////////////////
class BaseBoxLayer(Layer) :
	pass
	
class HLOCLayer(BaseBoxLayer) :
	def setColorMethod(self, colorMethod, riseColor, fallColor = -1, leadValue = -1.7E308) :
		_r("HLOCLayer.setColorMethod", self.this, colorMethod, riseColor, fallColor, leadValue)
			
class CandleStickLayer(BaseBoxLayer) :
	pass

class BoxWhiskerLayer(BaseBoxLayer) :
	defaultArgs = {
		"setBoxColors":(None, 2, None),
		"addPredictionBand":(None, 7, Transparent, 1, -1, -1, -1),
	}
	pass

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to vectorlayer.h
#///////////////////////////////////////////////////////////////////////////////////
class VectorLayer(Layer) :
	defaultArgs = {
		"setVector":(None, 3, PixelScale),
		"setIconSize":(None, 2, 0),
		"setVectorMargin":(None, 2, NoValue)
	}	
	def setArrowHead(self, width, height = 0) :
		if argIsArray(width) :
			self.setArrowHead2(width)
		else :
			_r("VectorLayer.setArrowHead", self.this, width, height)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to contourlayer.h
#///////////////////////////////////////////////////////////////////////////////////
class ContourLayer(Layer) :
	defaultArgs = {
		"setContourColor":(None, 2, -1),
		"setContourWidth":(None, 2, -1),
		"setColorAxis":(ColorAxis, 5),
		"colorAxis":(ColorAxis, 0)
	}	

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to xychart.h
#///////////////////////////////////////////////////////////////////////////////////
class PlotArea(AutoMethod) :
	defaultArgs = {
		"setBackground":(None, 3, -1, -1),
		"setBackground2":(None, 2, Center),
		"set4QBgColor":(None, 5, -1),
		"setAltBgColor":(None, 4, -1),
		"setGridColor":(None, 4, Transparent, -1, -1),
		"setGridWidth":(None, 4, -1, -1, -1)
	}
	def setGridAxis(self, xAxis, yAxis) :
		_r("PlotArea.setGridAxis", self.this, decodePtr(xAxis), decodePtr(yAxis))
	def moveGridBefore(self, layer = None) :
		_r("PlotArea.moveGridBefore", self.this, decodePtr(layer))

class XYChart(BaseChart) :
	defaultArgs = {
		"yAxis":(Axis, 0),	
		"yAxis2":(Axis, 0),	
		"syncYAxis":(Axis, 2, 1, 0),	
		"setYAxisOnRight":(None, 1, 1),
		"setXAxisOnTop":(None, 1, 1),
		"xAxis":(Axis, 0),	
		"xAxis2":(Axis, 0),	
		"addAxis":(Axis, 2),
		"swapXY":(None, 1, 1),
		"setPlotArea":(PlotArea, 9, Transparent, -1, -1, 0xc0c0c0, Transparent),
		"getPlotArea":(PlotArea, 0),
		"setClipping":(None, 1, 0),
		"addBarLayer2":(BarLayer, 2, Side, 0),
		"addBarLayer3":(BarLayer, 4, None, None, 0),
		"addLineLayer2":(LineLayer, 2, Overlay, 0),
		"addAreaLayer2":(AreaLayer, 2, Stack, 0),
		"addHLOCLayer2":(HLOCLayer, 0),
		"addScatterLayer":(ScatterLayer, 7, "", SquareSymbol, 5, -1, -1),
		"addCandleStickLayer":(CandleStickLayer, 7, 0xffffff, 0x0, LineColor),
		"addBoxWhiskerLayer":(BoxWhiskerLayer, 8, None, None, None, -1, LineColor, LineColor),
		"addBoxWhiskerLayer2":(BoxWhiskerLayer, 8, None, None, None, None, 0.5, None),
		"addBoxLayer":(BoxWhiskerLayer, 4, -1, ""),
		"addTrendLayer":(TrendLayer, 4, -1, "", 0),
		"addTrendLayer2":(TrendLayer, 5, -1, "", 0),
		"addSplineLayer":(SplineLayer, 3, None, -1, ""),
		"addStepLineLayer":(StepLineLayer, 3, None, -1, ""),
		"addInterLineLayer":(InterLineLayer, 4, -1),
		"addVectorLayer":(VectorLayer, 7, PixelScale, -1, ""),
		"addContourLayer":(ContourLayer, 3),
		"setAxisAtOrigin":(None, 2, XYAxisAtOrigin, 0),
		"setTrimData":(None, 2, 0x7fffffff),
		"packPlotArea":(None, 6, 0, 0)
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("XYChart.create", width, height, bgColor, edgeColor, raisedEffect)
	def addBarLayer(self, data = None, color = -1, name = "", depth = 0) :
		if data != None :
			return BarLayer(_r("XYChart.addBarLayer", self.this, data, color, name, depth))
		else :
			return self.addBarLayer2()
	def addLineLayer(self, data = None, color = -1, name = "", depth = 0) :
		if data != None :
			return LineLayer(_r("XYChart.addLineLayer", self.this, data, color, name, depth))
		else :
			return self.addLineLayer2()
	def addAreaLayer(self, data = None, color = -1, name = "", depth = 0) :
		if data != None :
			return AreaLayer(_r("XYChart.addAreaLayer", self.this, data, color, name, depth))
		else :
			return self.addAreaLayer2()
	def addHLOCLayer(self, highData = None, lowData = None, openData = None, closeData = None, 
		upColor = -1, downColor = -1, colorMode = -1, leadValue = -1.7E308) :
		if highData != None :
			return HLOCLayer(_r("XYChart.addHLOCLayer3", self.this, highData, lowData, openData, closeData, upColor, downColor, colorMode, leadValue))
		else :
			return self.addHLOCLayer2()
	addHLOCLayer3 = addHLOCLayer
	def getYCoor(self, value, yAxis = None) :
		return _r("XYChart.getYCoor", self.this, value, decodePtr(yAxis))
	def yZoneColor(self, threshold, belowColor, aboveColor, yAxis = None) :
		return _r("XYChart.yZoneColor", self.this, threshold, belowColor, aboveColor, decodePtr(yAxis))

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to surfacechart.h
#///////////////////////////////////////////////////////////////////////////////////
class SurfaceChart(BaseChart) :
	defaultArgs = {
		"setViewAngle":(None, 3, 0, 0),	
		"setInterpolation":(None, 3, -1, 1),	
		"setShadingMode":(None, 2, 1),	
		"setSurfaceAxisGrid":(None, 4, -1, -1, -1),
		"setSurfaceDataGrid":(None, 2, -1),
		"setContourColor":(None, 2, -1),
		"xAxis":(Axis, 0),	
		"yAxis":(Axis, 0),
		"zAxis":(Axis, 0),	
		"setColorAxis":(ColorAxis, 5),	
		"colorAxis":(ColorAxis, 0),
		"setWallColor":(None, 4, -1, -1, -1),
		"setWallThickness":(None, 3, -1, -1),
		"setWallGrid":(None, 6, -1, -1, -1, -1, -1)
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("SurfaceChart.create", width, height, bgColor, edgeColor, raisedEffect)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to polarchart.h
#///////////////////////////////////////////////////////////////////////////////////
class PolarLayer(AutoMethod) :
	defaultArgs = {
		"setData":(None, 3, -1, ""),
		"setSymbolScale":(None, 2, PixelScale),
		"getImageCoor":(None, 3, 0, 0),
		"getHTMLImageMap":(None, 5, "", "", 0, 0),
		"setDataLabelStyle":(TextBox, 4, "", 8, TextColor, 0),
		"addCustomDataLabel":(TextBox, 6, "", 8, TextColor, 0),
		"setDataSymbol4":(None, 4, 11, -1, -1),
		"setHTMLImageMap":(None, 3, "", "")
	}
	def setDataSymbol(self, symbol, size = None, fillColor = -1, edgeColor = -1, lineWidth = 1) :
		if argIsArray(symbol) :
			if size == None :
				size = 11
			self.setDataSymbol4(symbol, size, fillColor, edgeColor)
			return
		if size == None :
			try :
				symbol = int(symbol)
				size = 7
			except :
				self.setDataSymbol2(symbol)
				return
		_r("PolarLayer.setDataSymbol", self.this, symbol, size, fillColor, edgeColor, lineWidth)
	def setDataSymbol2(self, image) :
		if hasattr(image, "this") :
			self.setDataSymbol3(image)
		else :
			_r("PolarLayer.setDataSymbol2", self.this, image)
	def setDataSymbol3(self, image) :
		_r("PolarLayer.setDataSymbol3", self.this, image.this)
	
class PolarAreaLayer(PolarLayer) :
	pass

class PolarLineLayer(PolarLayer) :
	defaultArgs = {
		"setGapColor":(None, 2, -1)
	}

class PolarSplineLineLayer(PolarLineLayer) :
	pass

class PolarSplineAreaLayer(PolarAreaLayer) :
	pass

class PolarVectorLayer(PolarLayer) :
	defaultArgs = {
		"setVector":(None, 3, PixelScale),
		"setIconSize":(None, 2, 0),
		"setVectorMargin":(None, 2, NoValue)
	}	
	def setArrowHead(self, width, height = 0) :
		if argIsArray(width) :
			self.setArrowHead2(width)
		else :
			_r("PolarVectorLayer.setArrowHead", self.this, width, height)

class PolarChart(BaseChart) :
	defaultArgs = {
		"setPlotArea":(None, 6, Transparent, Transparent, 1),	
		"setPlotAreaBg":(None, 3, -1, 1),	
		"setGridColor":(None, 4, LineColor, 1, LineColor, 1),
		"setGridStyle":(None, 2, 1),
		"setStartAngle":(None, 2, 1),
		"angularAxis":(AngularAxis, 0),
		"radialAxis":(Axis, 0),	
		"addAreaLayer":(PolarAreaLayer, 3, -1, ""),
		"addLineLayer":(PolarLineLayer, 3, -1, ""),
		"addSplineLineLayer":(PolarSplineLineLayer, 3, -1, ""),
		"addSplineAreaLayer":(PolarSplineAreaLayer, 3, -1, ""),
		"addVectorLayer":(PolarVectorLayer, 7, PixelScale, -1, "")
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("PolarChart.create", width, height, bgColor, edgeColor, raisedEffect)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to pyramidchart.h
#///////////////////////////////////////////////////////////////////////////////////
class PyramidLayer(AutoMethod) :
	defaultArgs = {
		"setCenterLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setRightLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setLeftLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setJoinLine":(None, 2, -1),
		"setJoinLineGap":(None, 3, -0x7fffffff, -0x7fffffff),
		"setLayerBorder":(None, 2, -1)
	}	
	
class PyramidChart(BaseChart) :
	defaultArgs = {
		"setFunnelSize":(None, 6, 0.2, 0.3),
		"setData":(None, 2, None),
		"setCenterLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setRightLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setLeftLabel":(TextBox, 4, "{skip}", "{skip}", -1, -1),
		"setViewAngle":(None, 3, 0, 0),
		"setLighting":(None, 4, 0.5, 0.5, 1, 8),
		"setJoinLine":(None, 2, -1),
		"setJoinLineGap":(None, 3, -0x7fffffff, -0x7fffffff),
		"setLayerBorder":(None, 2, -1),
		"getLayer":(PyramidLayer, 1)
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("PyramidChart.create", width, height, bgColor, edgeColor, raisedEffect)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to meters.h
#///////////////////////////////////////////////////////////////////////////////////
class MeterPointer(AutoMethod) :
	defaultArgs = {
		"setColor":(None, 2, -1),
		"setShape2":(None, 3, NoValue, NoValue)
	}
	def setShape(self, pointerType, lengthRatio = NoValue, widthRatio = NoValue) :
		_r(encodeIfArray("MeterPointer.setShape", pointerType), self.this, pointerType, lengthRatio, widthRatio)
	
class BaseMeter(BaseChart) :
	defaultArgs = {
		"addPointer":(MeterPointer, 3, LineColor, -1),
		"setScale3":(None, 4, ""),
		"setLabelStyle":(TextBox, 4, "bold", -1, TextColor, 0),
		"setLabelPos":(None, 2, 0),
		"setTickLength":(None, 3, -0x7fffffff, -0x7fffffff),
		"setLineWidth":(None, 4, 1, 1, 1),
		"setMeterColors":(None, 3, -1, -1)
	}
	def setScale(self, lowerLimit, upperLimit, majorTickInc = 0, minorTickInc = 0, microTickInc = 0) :
		if argIsArray(majorTickInc) :
			if minorTickInc != 0 :
				self.setScale3(lowerLimit, upperLimit, majorTickInc, minorTickInc)
			else :
				self.setScale2(lowerLimit, upperLimit, majorTickInc)
		else :
			_r("BaseMeter.setScale", self.this, lowerLimit, upperLimit, majorTickInc, minorTickInc, microTickInc)

class AngularMeter(BaseMeter) :
	defaultArgs = {
		"addRing":(None, 4, -1),
		"addRingSector":(None, 6, -1),
		"setCap":(None, 3, LineColor),
		"addZone2":(None, 4, -1)
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("AngularMeter.create", width, height, bgColor, edgeColor, raisedEffect)
	def addZone(self, startValue, endValue, startRadius, endRadius = -1, fillColor = None, edgeColor = -1) :
		if fillColor == None:
			self.addZone2(startValue, endValue, startRadius, endRadius)
		else :
			_r("AngularMeter.addZone", self.this, startValue, endValue, startRadius, endRadius, fillColor, edgeColor)

class LinearMeter(BaseMeter) :
	defaultArgs = {
		"setMeter":(None, 6, Left, 0),
		"setRail":(None, 3, 2, 6),
		"addZone":(TextBox, 4, "")
	}
	def __init__(self, width, height, bgColor = BackgroundColor, edgeColor = Transparent, raisedEffect = 0) :
		self.this = _r("LinearMeter.create", width, height, bgColor, edgeColor, raisedEffect)

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to chartdir.h
#///////////////////////////////////////////////////////////////////////////////////
def getCopyright() :
	return _r("getCopyright")

def getVersion() :
	return _r("getVersion")

def getDescription() :
	return _r("getDescription")

def getBootLog() :
	return _r("getBootLog")

def libgTTFTest(font = "", fontIndex = 0, fontHeight = 8, fontWidth = 8, angle = 0) :
	return _r("testFont", font, fontIndex, fontHeight, fontWidth, angle)

def testFont(font = "", fontIndex = 0, fontHeight = 8, fontWidth = 8, angle = 0) :
	return _r("testFont", font, fontIndex, fontHeight, fontWidth, angle)

def setLicenseCode(licCode) :
    return _r("setLicenseCode", licCode)

def chartTime(y, m = None, d = 1, h = 0, n = 0, s = 0) :
	if m == None :
		return chartTime2(y)
	else :
		return _r("chartTime", y, m, d, h, n, s)

def chartTime2(t) :
	return _r("chartTime2", t)
	
def getChartYMD(t) :
	return _r("getChartYMD", t)
	
def getChartWeekDay(t) :
	return (long(t) / 86400 + 1) % 7

#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to rantable.h
#///////////////////////////////////////////////////////////////////////////////////
class RanTable(AutoMethod) :
	defaultArgs = {
		"setCol2":(None, 6, -1E+308, 1E+308),
		"setDateCol":(None, 4, 0),
		"setHLOCCols":(None, 6, 0, 1E+308)
		}
	this = None
	def __init__(self, seed, noOfCols, noOfRows) :
		self.this = _r("RanTable.create", seed, noOfCols, noOfRows)
	def __del__(self) :
		if self.this != None :
			_r("RanTable.destroy", self.this)
	def setCol(self, colNo, minValue, maxValue, p4 = None, p5 = -1E+308, p6 = 1E+308) :
		if p4 == None :
			_r("RanTable.setCol", self.this, colNo, minValue, maxValue)
		else :
			self.setCol2(colNo, minValue, maxValue, p4, p5, p6)
	
class FinanceSimulator(AutoMethod):
	this = None
	def __init__(self, seed, startTime, endTime, resolution) :
		if type(seed) == type("") :
			self.this = _r("FinanceSimulator.create2", seed, startTime, endTime, resolution)
		else :
			self.this = _r("FinanceSimulator.create", seed, startTime, endTime, resolution)
	def __del__(self) :
		if self.this != None :
			_r("FinanceSimulator.destroy", self.this)
	
#///////////////////////////////////////////////////////////////////////////////////
#//	bindings to datafilter.h
#///////////////////////////////////////////////////////////////////////////////////
class ArrayMathMethodWrapper(MethodWrapper) :
	def __call__(self, *args) :
		ret = apply(MethodWrapper.__call__, (self,) + args)
		if ret == self.obj.this :
			return self.obj
		else :
			return ret

class ArrayMath :
	defaultArgs = {
		"shift":(None, 2, 1, NoValue),
		"delta":(None, 1, 1),
		"rate":(None, 1, 1),
		"trim":(None, 2, 0, -1),
		"insert":(None, 2, -1),
		"insert2":(None, 3, -1),
		"selectGTZ":(None, 2, None, 0),
		"selectGEZ":(None, 2, None, 0),
		"selectLTZ":(None, 2, None, 0),
		"selectLEZ":(None, 2, None, 0),
		"selectEQZ":(None, 2, None, 0),
		"selectNEZ":(None, 2, None, 0),
		"selectStartOfHour":(None, 2, 1, 300),
		"selectStartOfDay":(None, 2, 1, 3 * 3600),
		"selectStartOfWeek":(None, 2, 1, 2 * 86400),
		"selectStartOfMonth":(None, 2, 1, 5 * 86400),
		"selectStartOfYear":(None, 2, 1, 60 * 86400),
		"movCorr":(None, 2, None),
		"lowess":(None, 2, 0.25, 0),
		"lowess2":(None, 3, 0.25, 0),
		"selectRegularSpacing":(None, 3, 0, 0),
		"aggregate":(None, 3, 50)
		}
	this = None
	def __init__(self, a) :
		self.this = _r("ArrayMath.create", a)
	def __del__(self) :
		if self.this != None :
			_r("ArrayMath.destroy", self.this)
	def __getattr__(self, name) :
		if name[:2] == "__" :
			raise AttributeError 
		return ArrayMathMethodWrapper(self, name)
	def binOp(self, op, b) :
		if argIsArray(b) :
			_r("ArrayMath." + op, self.this, b)
			return self
		else :
			return getattr(self, op + "2")(b)
	def add(self, b) :
		return self.binOp("add", b)
	def sub(self, b) :
		return self.binOp("sub", b)
	def mul(self, b) :
		return self.binOp("mul", b)
	def div(self, b) :
		return self.binOp("div", b)

#///////////////////////////////////////////////////////////////////////////////////
#//	Utility functions
#///////////////////////////////////////////////////////////////////////////////////

#
#	Normalize the path and remove trailing slash
#
def normalizePath(path) :
	path = string.replace(path, "\\", "/")
	if path[-1] == "/" :
		path = path[:-1]
	return path
	
#
#	Create a unique temporary file name and automatically removes old temporary files 
#
def tmpFile(path = "/tmp/tmp_charts", lifeTime = 600) :
	#for compatibility with ChartDirector Ver 2.5
	path = normalizePath(path)
	return path + "/" + tmpFile2(path, lifeTime, "")

def tmpFile2(path, lifeTime, ext) :
	#avoid checking for old files too frequently
	if lifeTime >= 0:
		currentTime = time.time()
		timeStampFile = path + "/__cd__lastcheck.tmp"
		try :
			lastCheck = abs(currentTime - os.stat(timeStampFile)[8])
			if lastCheck < lifeTime and lastCheck < 10 :
				lifeTime = -1
			else :
				os.utime(timeStampFile, (currentTime, currentTime))
		except :
			try :
				if not os.path.exists(timeStampFile) :
					f = open(timeStampFile, "wb")
					f.write(time.asctime())
					f.close()
			except :
				pass
	
	#remove old temporary files
	if lifeTime >= 0 :
		try :
			garbage = []
			for p in os.listdir(path) :
				if p[:4] != "cd__" :
					continue
				filename = "%s/%s" % (path, p)
				filestat = os.stat(filename)
				if abs(currentTime - filestat[9]) > lifeTime :
					garbage.append(filename)
			for p in garbage :
				os.unlink(p)
		except :
			#make the directory in case it does not exist
			fields = string.split(path, "/")
			if fields[0] == '' :
				fields[0:2] = ['/' + fields[1]]
			for i in range(0, len(fields)) :
				try :
					os.mkdir(string.join(fields[:i + 1], "/"), 0777)
				except :
					pass	
				
	#create unique file name
	seqNo = 0
	while seqNo < 100 :
		if os.environ.has_key("UNIQUE_ID") :
			filename = "cd__%s%s_%s%s" % (os.environ["UNIQUE_ID"], time.time(), seqNo, ext)
		else :
			filename = "cd__%s%s%s%s_%s%s" % (os.environ.get("REMOTE_ADDR", ""), 
				os.environ.get("REMOTE_PORT", ""), os.getpid(), time.time(), seqNo, ext)
		if not os.path.exists(path + "/" + filename) :
			break
		seqNo = seqNo + 1

	return filename

#
#	Print in binary format
#
def binaryPrint(s) :
	try :
	    #Make sure we use binary mode if we are running on windows
	    import msvcrt
	    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
	except :
	    pass
	#use stdout instead of print because print will add an extra new line character at the end
	sys.stdout.write(s)


#///////////////////////////////////////////////////////////////////////////////////
#//	WebChartViewer implementation
#///////////////////////////////////////////////////////////////////////////////////
MouseUsageDefault = 0
MouseUsageScroll = 2
MouseUsageZoomIn = 3
MouseUsageZoomOut = 4
	
DirectionHorizontal = 0
DirectionVertical = 1
DirectionHorizontalVertical = 2

class WebChartViewer :

	_s = "_JsChartViewerState"
	_p = "cdPartialUpdate"
	_d = "cdDirectStream"

	def __init__(self, request, id) :
		self.this = _r("WebChartViewer.create")
		self.putAttrS(":id", id)
		self.request = request
		if request != None and id != None and request.has_key(id + self._s) :
			self.putAttrS(":state", request[id + self._s].value)
	def __del__(self) :
		if self.this != None :
			_r("WebChartViewer.destroy", self.this)
			
	def getRequest(self) :
		return self.request
	def getId(self) :
		return self.getAttrS(":id")
	
	def setImageUrl(self, url) :
		self.putAttrS(":url", url)
	def getImageUrl(self):
		return self.getAttrS(":url")
	
	def setImageMap(self, imageMap) :
		self.putAttrS(":map", imageMap)
	def getImageMap(self) :
		return self.getAttrS(":map")
		
	def setChartMetrics(self, metrics) :
		self.putAttrS(":metrics", metrics)
	def getChartMetrics(self) :
		return self.getAttrS(":metrics")
		
	def makeDelayedMapAsTmpFile(self, path, imageMap, compress = 0, timeout = 600):
		if compress :
			try:
			    if string.find(os.environ.get("HTTP_ACCEPT_ENCODING", ""), "gzip") == -1:
			        compress = 0
			except:
			    pass

		b = "<body><!--CD_MAP %s CD_MAP--></body>" % imageMap
		ext = ".map"
		if compress :
			b = _r("WebChartViewer.compressMap", self.this, b, 4)
			if b != None and len(b) > 2 and b[0:2] == "\x1f\x8b" :
				ext = ".map.gz"

		path = normalizePath(path)
		filename = tmpFile2(path, timeout, ext)
		if filename != "" :
			f = open(path + "/" + filename, "wb")
			f.write(b)
			f.close()	
		return filename
		
	def renderHTML(self, extraAttrs = None) :
		return _r("WebChartViewer.renderHTML", self.this, os.environ.get("SCRIPT_NAME", ""), os.environ.get("QUERY_STRING", ""), extraAttrs)	
	def partialUpdateChart(self, msg = None, timeout = 0) :
		return "Content-type: text/html; charset=utf-8\n\n" + _r("WebChartViewer.partialUpdateChart", self.this, msg, timeout)	
		
	def isPartialUpdateRequest(self) :
		return self.request != None and self.request.has_key(self._p)
	def isFullUpdateRequest(self) :
		if self.isPartialUpdateRequest() :
			return 0
		if self.request != None :
			for k in self.request.keys() :
				if k[-len(self._s):] == self._s:
					return 1
		return 0
	def isStreamRequest(self) :
		return self.request != None and self.request.has_key(self._d)
	def isViewPortChangedEvent(self) :
		return self.getAttrF(25, 0) != 0 
	def getSenderClientId(self) :
		if self.isPartialUpdateRequest() :
			return self.request[self._p].value
		elif self.isStreamRequest() :
			return self.request[self._d].value
		else :
			return None

	def getAttrS(self, attr, defaultValue = "") :
		return _r("WebChartViewer.getAttrS", self.this, str(attr), str(defaultValue))
	def getAttrF(self, attr, defaultValue = 0) :
		return _r("WebChartViewer.getAttrF", self.this, str(attr), float(defaultValue))
	def putAttrF(self, attr, value) :
		_r("WebChartViewer.putAttrF", self.this, str(attr), float(value))
	def putAttrS(self, attr, value) :
		_r("WebChartViewer.putAttrS", self.this, str(attr), str(value))

	def getViewPortLeft(self) :
		return self.getAttrF(4, 0)
	def setViewPortLeft(self, left) :
		self.putAttrF(4, left)

	def getViewPortTop(self) :
		return self.getAttrF(5, 0)
	def setViewPortTop(self, top) :
		self.putAttrF(5, top)

	def getViewPortWidth(self) :
		return self.getAttrF(6, 1)
	def setViewPortWidth(self, width) :
		self.putAttrF(6, width)

	def getViewPortHeight(self) :
		return self.getAttrF(7, 1)
	def setViewPortHeight(self, height) :
		self.putAttrF(7, height)

	def getSelectionBorderWidth(self) :
		return int(self.getAttrF(8, 2))
	def setSelectionBorderWidth(self, lineWidth) :
		self.putAttrF(8, lineWidth)

	def getSelectionBorderColor(self) :
		return self.getAttrS(9, "Black")
	def setSelectionBorderColor(self, color) :
		self.putAttrS(9, color)

	def getMouseUsage(self) :
		return int(self.getAttrF(10, MouseUsageDefault))
	def setMouseUsage(self, usage) :
		self.putAttrF(10, usage)

	def getScrollDirection(self) :
		return int(self.getAttrF(11, DirectionHorizontal))
	def setScrollDirection(self, direction) :
		self.putAttrF(11, direction)

	def getZoomDirection(self) :
		return int(self.getAttrF(12, DirectionHorizontal))
	def setZoomDirection(self, direction) :
		self.putAttrF(12, direction)

	def getZoomInRatio(self) :
		return self.getAttrF(13, 2)
	def setZoomInRatio(self, ratio) :
		if ratio > 0 : self.putAttrF(13, ratio)

	def getZoomOutRatio(self) :
		return self.getAttrF(14, 0.5)
	def setZoomOutRatio(self, ratio) :
		if ratio > 0 : self.putAttrF(14, ratio)

	def getZoomInWidthLimit(self) :
		return self.getAttrF(15, 0.01)
	def setZoomInWidthLimit(self, limit) :
		self.putAttrF(15, limit)

	def getZoomOutWidthLimit(self) :
		return self.getAttrF(16, 1)
	def setZoomOutWidthLimit(self, limit) :
		self.putAttrF(16, limit)

	def getZoomInHeightLimit(self) :
		return self.getAttrF(17, 0.01)
	def setZoomInHeightLimit(self, limit) :
		self.putAttrF(17, limit)

	def getZoomOutHeightLimit(self) :
		return self.getAttrF(18, 1)
	def setZoomOutHeightLimit(self, limit) :
		self.putAttrF(18, limit)
		
	def getMinimumDrag(self) :
		return int(self.getAttrF(19, 5))
	def setMinimumDrag(self, offset) :
		self.putAttrF(19, offset)

	def getZoomInCursor(self) :
		return self.getAttrS(20, "")
	def setZoomInCursor(self, cursor) :
		self.putAttrS(20, cursor)

	def getZoomOutCursor(self) :
		return self.getAttrS(21, "")
	def setZoomOutCursor(self, cursor) :
		self.putAttrS(21, cursor)

	def getScrollCursor(self) :
		return self.getAttrS(22, "")
	def setScrollCursor(self, cursor) :
		self.putAttrS(22, cursor)

	def getNoZoomCursor(self) :
		return self.getAttrS(26, "")
	def setNoZoomCursor(self, cursor) :
		self.putAttrS(26, cursor)

	def getCustomAttr(self, key) :
		return self.getAttrS(key, "")
	def setCustomAttr(self, key, value) :
		self.putAttrS(key, value)
