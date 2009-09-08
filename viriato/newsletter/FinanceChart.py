#!/usr/bin/python
from pychartdir import *

#/////////////////////////////////////////////////////////////////////////////////////////////////
# Copyright 2008 Advanced Software Engineering Limited
#
# ChartDirector FinanceChart class library
#     - Requires ChartDirector Ver 5.0 or above
#
# You may use and modify the code in this file in your application, provided the code and
# its modifications are used only in conjunction with ChartDirector. Usage of this software
# is subjected to the terms and condition of the ChartDirector license.
#/////////////////////////////////////////////////////////////////////////////////////////////////

#/ <summary>
#/ Represents a Financial Chart
#/ </summary>
class FinanceChart(MultiChart) :

    m_totalWidth = 0
    m_totalHeight = 0
    m_antiAlias = 1
    m_logScale = 0
    m_axisOnRight = 1

    m_leftMargin = 40
    m_rightMargin = 40
    m_topMargin = 30
    m_bottomMargin = 35

    m_plotAreaBgColor = 0xffffff
    m_plotAreaBorder = 0x888888
    m_plotAreaGap = 2

    m_majorHGridColor = 0xdddddd
    m_minorHGridColor = 0xdddddd
    m_majorVGridColor = 0xdddddd
    m_minorVGridColor = 0xdddddd

    m_legendFont = "normal"
    m_legendFontSize = 8
    m_legendFontColor = TextColor
    m_legendBgColor = 0x80ccccccL

    m_yAxisFont = "normal"
    m_yAxisFontSize = 8
    m_yAxisFontColor = TextColor
    m_yAxisMargin = 14

    m_xAxisFont = "normal"
    m_xAxisFontSize = 8
    m_xAxisFontColor = TextColor
    m_xAxisFontAngle = 0

    m_timeStamps = None
    m_highData = None
    m_lowData = None
    m_openData = None
    m_closeData = None
    m_volData = None
    m_volUnit = ""
    m_extraPoints = 0

    m_yearFormat = "{value|yyyy}"
    m_firstMonthFormat = "<*font=bold*>{value|mmm yy}"
    m_otherMonthFormat = "{value|mmm}"
    m_firstDayFormat = "<*font=bold*>{value|d mmm}"
    m_otherDayFormat = "{value|d}"
    m_firstHourFormat = "<*font=bold*>{value|d mmm\nh:nna}"
    m_otherHourFormat = "{value|h:nna}"
    m_timeLabelSpacing = 50

    m_generalFormat = "P3"

    m_toolTipMonthFormat = "[{xLabel|mmm yyyy}]"
    m_toolTipDayFormat = "[{xLabel|mmm d, yyyy}]"
    m_toolTipHourFormat = "[{xLabel|mmm d, yyyy hh:nn:ss}]"

    m_mainChart = None
    m_currentChart = None

    #/ <summary>
    #/ Create a FinanceChart with a given width. The height will be automatically determined
    #/ as the chart is built.
    #/ </summary>
    #/ <param name="width">Width of the chart in pixels</param>
    def __init__(self, width) :
        MultiChart.__init__(self, width, 1)
        self.m_totalWidth = width

    #/ <summary>
    #/ Enable/Disable anti-alias. Enabling anti-alias makes the line smoother. Disabling
    #/ anti-alias make the chart file size smaller, and so can be downloaded faster
    #/ through the Internet. The default is to enable anti-alias.
    #/ </summary>
    #/ <param name="antiAlias">True to enable anti-alias. False to disable anti-alias.</param>
    def enableAntiAlias(self, antiAlias) :
        self.m_antiAlias = antiAlias

    #/ <summary>
    #/ Set the margins around the plot area.
    #/ </summary>
    #/ <param name="m_leftMargin">The distance between the plot area and the chart left edge.</param>
    #/ <param name="m_topMargin">The distance between the plot area and the chart top edge.</param>
    #/ <param name="m_rightMargin">The distance between the plot area and the chart right edge.</param>
    #/ <param name="m_bottomMargin">The distance between the plot area and the chart bottom edge.</param>
    def setMargins(self, leftMargin, topMargin, rightMargin, bottomMargin) :
        self.m_leftMargin = leftMargin
        self.m_rightMargin = rightMargin
        self.m_topMargin = topMargin
        self.m_bottomMargin = bottomMargin

    #/ <summary>
    #/ Add a text title above the plot area. You may add multiple title above the plot area by
    #/ calling this method multiple times.
    #/ </summary>
    #/ <param name="alignment">The alignment with respect to the region that is on top of the
    #/ plot area.</param>
    #/ <param name="text">The text to add.</param>
    #/ <returns>The TextBox object representing the text box above the plot area.</returns>
    def addPlotAreaTitle(self, alignment, text) :
        ret = self.addText(self.m_leftMargin, 0, text, "bold", 10, TextColor, alignment)
        ret.setSize(self.m_totalWidth - self.m_leftMargin - self.m_rightMargin + 1,
            self.m_topMargin - 1)
        ret.setMargin(0)
        return ret

    #/ <summary>
    #/ Set the plot area style. The default is to use pale yellow 0xfffff0 as the background,
    #/ and light grey 0xdddddd as the grid lines.
    #/ </summary>
    #/ <param name="bgColor">The plot area background color.</param>
    #/ <param name="majorHGridColor">Major horizontal grid color.</param>
    #/ <param name="majorVGridColor">Major vertical grid color.</param>
    #/ <param name="minorHGridColor">Minor horizontal grid color. In current version, minor
    #/ horizontal grid is not used.</param>
    #/ <param name="minorVGridColor">Minor vertical grid color.</param>
    def setPlotAreaStyle(self, bgColor, majorHGridColor, majorVGridColor, minorHGridColor,
        minorVGridColor) :
        self.m_plotAreaBgColor = bgColor
        self.m_majorHGridColor = majorHGridColor
        self.m_majorVGridColor = majorVGridColor
        self.m_minorHGridColor = minorHGridColor
        self.m_minorVGridColor = minorVGridColor

    #/ <summary>
    #/ Set the plot area border style. The default is grey color (888888), with a gap
    #/ of 2 pixels between charts.
    #/ </summary>
    #/ <param name="borderColor">The color of the border.</param>
    #/ <param name="borderGap">The gap between two charts.</param>
    def setPlotAreaBorder(self, borderColor, borderGap) :
        self.m_plotAreaBorder = borderColor
        self.m_plotAreaGap = borderGap

    #/ <summary>
    #/ Set legend style. The default is Arial 8 pt black color, with light grey background.
    #/ </summary>
    #/ <param name="font">The font of the legend text.</param>
    #/ <param name="fontSize">The font size of the legend text in points.</param>
    #/ <param name="fontColor">The color of the legend text.</param>
    #/ <param name="bgColor">The background color of the legend box.</param>
    def setLegendStyle(self, font, fontSize, fontColor, bgColor) :
        self.m_legendFont = font
        self.m_legendFontSize = fontSize
        self.m_legendFontColor = fontColor
        self.m_legendBgColor = bgColor

    #/ <summary>
    #/ Set x-axis label style. The default is Arial 8 pt black color no rotation.
    #/ </summary>
    #/ <param name="font">The font of the axis labels.</param>
    #/ <param name="fontSize">The font size of the axis labels in points.</param>
    #/ <param name="fontColor">The color of the axis labels.</param>
    #/ <param name="fontAngle">The rotation of the axis labels.</param>
    def setXAxisStyle(self, font, fontSize, fontColor, fontAngle) :
        self.m_xAxisFont = font
        self.m_xAxisFontSize = fontSize
        self.m_xAxisFontColor = fontColor
        self.m_xAxisFontAngle = fontAngle

    #/ <summary>
    #/ Set y-axis label style. The default is Arial 8 pt black color, with 13 pixels margin.
    #/ </summary>
    #/ <param name="font">The font of the axis labels.</param>
    #/ <param name="fontSize">The font size of the axis labels in points.</param>
    #/ <param name="fontColor">The color of the axis labels.</param>
    #/ <param name="axisMargin">The margin at the top of the y-axis in pixels (to leave
    #/ space for the legend box).</param>
    def setYAxisStyle(self, font, fontSize, fontColor, axisMargin) :
        self.m_yAxisFont = font
        self.m_yAxisFontSize = fontSize
        self.m_yAxisFontColor = fontColor
        self.m_yAxisMargin = axisMargin

    #/ <summary>
    #/ Set whether the main y-axis is on right of left side of the plot area. The default is
    #/ on right.
    #/ </summary>
    #/ <param name="b">True if the y-axis is on right. False if the y-axis is on left.</param>
    def setAxisOnRight(self, b) :
        self.m_axisOnRight = b

    #/ <summary>
    #/ Determines if log scale should be used for the main chart. The default is linear scale.
    #/ </summary>
    #/ <param name="b">True for using log scale. False for using linear scale.</param>
    def setLogScale(self, b) :
        self.m_logScale = b
        if self.m_mainChart != None :
            if self.m_logScale :
                self.m_mainChart.yAxis().setLogScale()
            else :
                self.m_mainChart.yAxis().setLinearScale()

    #/ <summary>
    #/ Set the date/time formats to use for the x-axis labels under various cases.
    #/ </summary>
    #/ <param name="yearFormat">The format for displaying labels on an axis with yearly ticks. The
    #/ default is "yyyy".</param>
    #/ <param name="firstMonthFormat">The format for displaying labels on an axis with monthly ticks.
    #/ This parameter applies to the first available month of a year (usually January) only, so it can
    #/ be formatted differently from the other labels.</param>
    #/ <param name="otherMonthFormat">The format for displaying labels on an axis with monthly ticks.
    #/ This parameter applies to months other than the first available month of a year.</param>
    #/ <param name="firstDayFormat">The format for displaying labels on an axis with daily ticks.
    #/ This parameter applies to the first available day of a month only, so it can be formatted
    #/ differently from the other labels.</param>
    #/ <param name="otherDayFormat">The format for displaying labels on an axis with daily ticks.
    #/ This parameter applies to days other than the first available day of a month.</param>
    #/ <param name="firstHourFormat">The format for displaying labels on an axis with hourly
    #/ resolution. This parameter applies to the first tick of a day only, so it can be formatted
    #/ differently from the other labels.</param>
    #/ <param name="otherHourFormat">The format for displaying labels on an axis with hourly.
    #/ resolution. This parameter applies to ticks at hourly boundaries, except the first tick
    #/ of a day.</param>
    def setDateLabelFormat(self, yearFormat, firstMonthFormat, otherMonthFormat, firstDayFormat,
        otherDayFormat, firstHourFormat, otherHourFormat) :
        if yearFormat != None :
            self.m_yearFormat = yearFormat
        if firstMonthFormat != None :
            self.m_firstMonthFormat = firstMonthFormat
        if otherMonthFormat != None :
            self.m_otherMonthFormat = otherMonthFormat
        if firstDayFormat != None :
            self.m_firstDayFormat = firstDayFormat
        if otherDayFormat != None :
            self.m_otherDayFormat = otherDayFormat
        if firstHourFormat != None :
            self.m_firstHourFormat = firstHourFormat
        if otherHourFormat != None :
            self.m_otherHourFormat = otherHourFormat

    #/ <summary>
    #/ Set the minimum label spacing between two labels on the time axis
    #/ </summary>
    #/ <param name="labelSpacing">The minimum label spacing in pixels.</param>
    def setDateLabelSpacing(self, labelSpacing) :
        if labelSpacing > 0 :
            self.m_timeLabelSpacing = labelSpacing
        else :
             self.m_timeLabelSpacing = 0

    #/ <summary>
    #/ Set the tool tip formats for display date/time
    #/ </summary>
    #/ <param name="monthFormat">The tool tip format to use if the data point spacing is one
    #/ or more months (more than 30 days).</param>
    #/ <param name="dayFormat">The tool tip format to use if the data point spacing is 1 day
    #/ to less than 30 days.</param>
    #/ <param name="hourFormat">The tool tip format to use if the data point spacing is less
    #/ than 1 day.</param>
    def setToolTipDateFormat(self, monthFormat, dayFormat, hourFormat) :
        if monthFormat != None :
            self.m_toolTipMonthFormat = monthFormat
        if dayFormat != None :
            self.m_toolTipDayFormat = dayFormat
        if hourFormat != None :
            self.m_toolTipHourFormat = hourFormat

    #/ <summary>
    #/ Get the tool tip format for display date/time
    #/ </summary>
    #/ <returns>The tool tip format string.</returns>
    def getToolTipDateFormat(self) :
        if self.m_timeStamps == None :
            return self.m_toolTipHourFormat
        if len(self.m_timeStamps) <= self.m_extraPoints :
            return self.m_toolTipHourFormat
        resolution = (self.m_timeStamps[len(self.m_timeStamps) - 1] - self.m_timeStamps[0]) / len(
            self.m_timeStamps)
        if resolution >= 30 * 86400 :
            return self.m_toolTipMonthFormat
        elif resolution >= 86400 :
            return self.m_toolTipDayFormat
        else :
            return self.m_toolTipHourFormat

    #/ <summary>
    #/ Set the number format for use in displaying values in legend keys and tool tips.
    #/ </summary>
    #/ <param name="formatString">The default number format.</param>
    def setNumberLabelFormat(self, formatString) :
        if formatString != None :
            self.m_generalFormat = formatString

    #/ <summary>
    #/ A utility function to compute triangular moving averages
    #/ </summary>
    #/ <param name="data">An array of numbers as input.</param>
    #/ <param name="period">The moving average period.</param>
    #/ <returns>An array representing the triangular moving average of the input array.</returns>
    def computeTriMovingAvg(self, data, period) :
        p = period / 2 + 1
        return ArrayMath(data).movAvg(p).movAvg(p).result()

    #/ <summary>
    #/ A utility function to compute weighted moving averages
    #/ </summary>
    #/ <param name="data">An array of numbers as input.</param>
    #/ <param name="period">The moving average period.</param>
    #/ <returns>An array representing the weighted moving average of the input array.</returns>
    def computeWeightedMovingAvg(self, data, period) :
        acc = ArrayMath(data)
        for i in range(2, period + 1) :
            acc.add(ArrayMath(data).movAvg(i).mul(i).result())
        return acc.div((1 + period) * period / 2).result()

    #/ <summary>
    #/ A utility function to obtain the first visible closing price.
    #/ </summary>
    #/ <returns>The first closing price.
    #/ are cd.NoValue.</returns>
    def firstCloseValue(self) :
        for i in range(self.m_extraPoints, len(self.m_closeData)) :
            if (self.m_closeData[i] != NoValue) and (self.m_closeData[i] != 0) :
                return self.m_closeData[i]
        return NoValue

    #/ <summary>
    #/ A utility function to obtain the last valid position (that is, position not
    #/ containing cd.NoValue) of a data series.
    #/ </summary>
    #/ <param name="data">An array of numbers as input.</param>
    #/ <returns>The last valid position in the input array, or -1 if all positions
    #/ are cd.NoValue.</returns>
    def lastIndex(self, data) :
        i = len(data) - 1
        while i >= 0 :
            if data[i] != NoValue :
                break
            i = i - 1
        return i

    #/ <summary>
    #/ Set the data used in the chart. If some of the data are not available, some artifical
    #/ values should be used. For example, if the high and low values are not available, you
    #/ may use closeData as highData and lowData.
    #/ </summary>
    #/ <param name="timeStamps">An array of dates/times for the time intervals.</param>
    #/ <param name="highData">The high values in the time intervals.</param>
    #/ <param name="lowData">The low values in the time intervals.</param>
    #/ <param name="openData">The open values in the time intervals.</param>
    #/ <param name="closeData">The close values in the time intervals.</param>
    #/ <param name="volData">The volume values in the time intervals.</param>
    #/ <param name="extraPoints">The number of leading time intervals that are not
    #/ displayed in the chart. These intervals are typically used for computing
    #/ indicators that require extra leading data, such as moving averages.</param>
    def setData(self, timeStamps, highData, lowData, openData, closeData, volData, extraPoints) :
        self.m_timeStamps = timeStamps
        self.m_highData = highData
        self.m_lowData = lowData
        self.m_openData = openData
        self.m_closeData = closeData
        if extraPoints > 0 :
            self.m_extraPoints = extraPoints
        else :
            self.m_extraPoints = 0

        #///////////////////////////////////////////////////////////////////////
        # Auto-detect volume units
        #///////////////////////////////////////////////////////////////////////
        maxVol = ArrayMath(volData).max()
        units = ["", "K", "M", "B"]
        unitIndex = len(units) - 1
        while (unitIndex > 0) and (maxVol < 1000**unitIndex) :
            unitIndex = unitIndex - 1

        self.m_volData = ArrayMath(volData).div(1000**unitIndex).result()
        self.m_volUnit = units[unitIndex]

    #////////////////////////////////////////////////////////////////////////////
    # Format x-axis labels
    #////////////////////////////////////////////////////////////////////////////
    def setXLabels(self, a) :
        a.setLabels2(self.m_timeStamps)
        if self.m_extraPoints < len(self.m_timeStamps) :
            tickStep = int((len(self.m_timeStamps) - self.m_extraPoints
                ) * self.m_timeLabelSpacing / (
                self.m_totalWidth - self.m_leftMargin - self.m_rightMargin)) + 1
            timeRangeInSeconds = self.m_timeStamps[len(self.m_timeStamps) - 1] - self.m_timeStamps[
                self.m_extraPoints]
            secondsBetweenTicks = timeRangeInSeconds / (
                self.m_totalWidth - self.m_leftMargin - self.m_rightMargin
                ) * self.m_timeLabelSpacing

            if secondsBetweenTicks * (len(self.m_timeStamps) - self.m_extraPoints
                ) <= timeRangeInSeconds :
                tickStep = 1
                if len(self.m_timeStamps) > 1 :
                    secondsBetweenTicks = self.m_timeStamps[len(self.m_timeStamps) - 1
                        ] - self.m_timeStamps[len(self.m_timeStamps) - 2]
                else :
                    secondsBetweenTicks = 86400

            if (secondsBetweenTicks > 360 * 86400) or ((secondsBetweenTicks > 90 * 86400) and (
                timeRangeInSeconds >= 720 * 86400)) :
                #yearly ticks
                a.setMultiFormat2(StartOfYearFilter(), self.m_yearFormat, tickStep)
            elif (secondsBetweenTicks >= 30 * 86400) or ((secondsBetweenTicks > 7 * 86400) and (
                timeRangeInSeconds >= 60 * 86400)) :
                #monthly ticks
                monthBetweenTicks = int(secondsBetweenTicks / 31 / 86400) + 1
                a.setMultiFormat(StartOfYearFilter(), self.m_firstMonthFormat, StartOfMonthFilter(
                    monthBetweenTicks), self.m_otherMonthFormat)
                a.setMultiFormat2(StartOfMonthFilter(), "-", 1, 0)
            elif (secondsBetweenTicks >= 86400) or ((secondsBetweenTicks > 6 * 3600) and (
                timeRangeInSeconds >= 86400)) :
                #daily ticks
                a.setMultiFormat(StartOfMonthFilter(), self.m_firstDayFormat, StartOfDayFilter(1,
                    0.5), self.m_otherDayFormat, tickStep)
            else :
                #hourly ticks
                a.setMultiFormat(StartOfDayFilter(1, 0.5), self.m_firstHourFormat,
                    StartOfHourFilter(1, 0.5), self.m_otherHourFormat, tickStep)

    #////////////////////////////////////////////////////////////////////////////
    # Create tool tip format string for showing OHLC data
    #////////////////////////////////////////////////////////////////////////////
    def getHLOCToolTipFormat(self) :
        return "title='%s Op:{open|%s}, Hi:{high|%s}, Lo:{low|%s}, Cl:{close|%s}'" % (
            self.getToolTipDateFormat(), self.m_generalFormat, self.m_generalFormat,
            self.m_generalFormat, self.m_generalFormat)

    #/ <summary>
    #/ Add the main chart - the chart that shows the HLOC data.
    #/ </summary>
    #/ <param name="height">The height of the main chart in pixels.</param>
    #/ <returns>An XYChart object representing the main chart created.</returns>
    def addMainChart(self, height) :
        self.m_mainChart = self.addIndicator(height)
        self.setMainChart(self.m_mainChart)
        self.m_mainChart.yAxis().setMargin(2 * self.m_yAxisMargin)
        if self.m_logScale :
            self.m_mainChart.yAxis().setLogScale()
        else :
            self.m_mainChart.yAxis().setLinearScale()
        return self.m_mainChart

    #/ <summary>
    #/ Add a candlestick layer to the main chart.
    #/ </summary>
    #/ <param name="upColor">The candle color for an up day.</param>
    #/ <param name="downColor">The candle color for a down day.</param>
    #/ <returns>The CandleStickLayer created.</returns>
    def addCandleStick(self, upColor, downColor) :
        self.addOHLCLabel(upColor, downColor, 1)
        ret = self.m_mainChart.addCandleStickLayer(self.m_highData, self.m_lowData, self.m_openData,
            self.m_closeData, upColor, downColor)
        ret.setHTMLImageMap("", "", self.getHLOCToolTipFormat())
        if len(self.m_highData) - self.m_extraPoints > 60 :
            ret.setDataGap(0)

        if len(self.m_highData) > self.m_extraPoints :
            expectedWidth = (self.m_totalWidth - self.m_leftMargin - self.m_rightMargin) / (len(
                self.m_highData) - self.m_extraPoints)
            if expectedWidth <= 5 :
                ret.setDataWidth(expectedWidth + 1 - expectedWidth % 2)

        return ret

    #/ <summary>
    #/ Add a HLOC layer to the main chart.
    #/ </summary>
    #/ <param name="upColor">The color of the HLOC symbol for an up day.</param>
    #/ <param name="downColor">The color of the HLOC symbol for a down day.</param>
    #/ <returns>The HLOCLayer created.</returns>
    def addHLOC(self, upColor, downColor) :
        self.addOHLCLabel(upColor, downColor, 0)
        ret = self.m_mainChart.addHLOCLayer(self.m_highData, self.m_lowData, self.m_openData,
            self.m_closeData)
        ret.setColorMethod(HLOCUpDown, upColor, downColor)
        ret.setHTMLImageMap("", "", self.getHLOCToolTipFormat())
        ret.setDataGap(0)
        return ret

    def addOHLCLabel(self, upColor, downColor, candleStickMode) :
        i = self.lastIndex(self.m_closeData)
        if i >= 0 :
            openValue = NoValue
            closeValue = NoValue
            highValue = NoValue
            lowValue = NoValue

            if i < len(self.m_openData) :
                openValue = self.m_openData[i]
            if i < len(self.m_closeData) :
                closeValue = self.m_closeData[i]
            if i < len(self.m_highData) :
                highValue = self.m_highData[i]
            if i < len(self.m_lowData) :
                lowValue = self.m_lowData[i]

            openLabel = ""
            closeLabel = ""
            highLabel = ""
            lowLabel = ""
            delim = ""
            if openValue != NoValue :
                openLabel = "Op:%s" % (self.formatValue(openValue, self.m_generalFormat))
                delim = ", "
            if highValue != NoValue :
                highLabel = "%sHi:%s" % (delim, self.formatValue(highValue, self.m_generalFormat))
                delim = ", "
            if lowValue != NoValue :
                lowLabel = "%sLo:%s" % (delim, self.formatValue(lowValue, self.m_generalFormat))
                delim = ", "
            if closeValue != NoValue :
                closeLabel = "%sCl:%s" % (delim, self.formatValue(closeValue, self.m_generalFormat))
                delim = ", "
            label = "%s%s%s%s" % (openLabel, highLabel, lowLabel, closeLabel)

            useUpColor = (closeValue >= openValue)
            if candleStickMode != 1 :
                closeChanges = ArrayMath(self.m_closeData).delta().result()
                lastChangeIndex = self.lastIndex(closeChanges)
                useUpColor = (lastChangeIndex < 0)
                if useUpColor != 1 :
                    useUpColor = (closeChanges[lastChangeIndex] >= 0)

            udcolor = downColor
            if useUpColor :
                udcolor = upColor
            self.m_mainChart.getLegend().addKey(label, udcolor)

    #/ <summary>
    #/ Add a closing price line on the main chart.
    #/ </summary>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addCloseLine(self, color) :
        return self.addLineIndicator2(self.m_mainChart, self.m_closeData, color, "Closing Price")

    #/ <summary>
    #/ Add a weight close line on the main chart.
    #/ </summary>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addWeightedClose(self, color) :
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.m_highData).add(
            self.m_lowData).add(self.m_closeData).add(self.m_closeData).div(4).result(), color,
            "Weighted Close")

    #/ <summary>
    #/ Add a typical price line on the main chart.
    #/ </summary>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addTypicalPrice(self, color) :
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.m_highData).add(
            self.m_lowData).add(self.m_closeData).div(3).result(), color, "Typical Price")

    #/ <summary>
    #/ Add a median price line on the main chart.
    #/ </summary>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addMedianPrice(self, color) :
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.m_highData).add(
            self.m_lowData).div(2).result(), color, "Median Price")

    #/ <summary>
    #/ Add a simple moving average line on the main chart.
    #/ </summary>
    #/ <param name="period">The moving average period</param>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addSimpleMovingAvg(self, period, color) :
        label = "SMA (%s)" % (period)
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.m_closeData).movAvg(period
            ).result(), color, label)

    #/ <summary>
    #/ Add an exponential moving average line on the main chart.
    #/ </summary>
    #/ <param name="period">The moving average period</param>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addExpMovingAvg(self, period, color) :
        label = "EMA (%s)" % (period)
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.m_closeData).expAvg(2.0 / (
            period + 1)).result(), color, label)

    #/ <summary>
    #/ Add a triangular moving average line on the main chart.
    #/ </summary>
    #/ <param name="period">The moving average period</param>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addTriMovingAvg(self, period, color) :
        label = "TMA (%s)" % (period)
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.computeTriMovingAvg(
            self.m_closeData, period)).result(), color, label)

    #/ <summary>
    #/ Add a weighted moving average line on the main chart.
    #/ </summary>
    #/ <param name="period">The moving average period</param>
    #/ <param name="color">The color of the line.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addWeightedMovingAvg(self, period, color) :
        label = "WMA (%s)" % (period)
        return self.addLineIndicator2(self.m_mainChart, ArrayMath(self.computeWeightedMovingAvg(
            self.m_closeData, period)).result(), color, label)

    #/ <summary>
    #/ Add a parabolic SAR indicator to the main chart.
    #/ </summary>
    #/ <param name="accInitial">Initial acceleration factor</param>
    #/ <param name="accIncrement">Acceleration factor increment</param>
    #/ <param name="accMaximum">Maximum acceleration factor</param>
    #/ <param name="symbolType">The symbol used to plot the parabolic SAR</param>
    #/ <param name="symbolSize">The symbol size in pixels</param>
    #/ <param name="fillColor">The fill color of the symbol</param>
    #/ <param name="edgeColor">The edge color of the symbol</param>
    #/ <returns>The LineLayer object representing the layer created.</returns>
    def addParabolicSAR(self, accInitial, accIncrement, accMaximum, symbolType, symbolSize,
        fillColor, edgeColor) :
        isLong = 1
        acc = accInitial
        extremePoint = 0
        psar = [0] * len(self.m_lowData)

        i_1 = -1
        i_2 = -1

        for i in range(0, len(self.m_lowData)) :
            psar[i] = NoValue
            if (self.m_lowData[i] != NoValue) and (self.m_highData[i] != NoValue) :
                if (i_1 >= 0) and (i_2 < 0) :
                    if self.m_lowData[i_1] <= self.m_lowData[i] :
                        psar[i] = self.m_lowData[i_1]
                        isLong = 1
                        if self.m_highData[i_1] > self.m_highData[i] :
                            extremePoint = self.m_highData[i_1]
                        else :
                            extremePoint = self.m_highData[i]
                    else :
                        extremePoint = self.m_lowData[i]
                        isLong = 0
                        if self.m_highData[i_1] > self.m_highData[i] :
                            psar[i] = self.m_highData[i_1]
                        else :
                            psar[i] = self.m_highData[i]
                elif (i_1 >= 0) and (i_2 >= 0) :
                    if acc > accMaximum :
                        acc = accMaximum

                    psar[i] = psar[i_1] + acc * (extremePoint - psar[i_1])

                    if isLong :
                        if self.m_lowData[i] < psar[i] :
                            isLong = 0
                            psar[i] = extremePoint
                            extremePoint = self.m_lowData[i]
                            acc = accInitial
                        else :
                            if self.m_highData[i] > extremePoint :
                                extremePoint = self.m_highData[i]
                                acc = acc + accIncrement

                            if self.m_lowData[i_1] < psar[i] :
                                psar[i] = self.m_lowData[i_1]
                            if self.m_lowData[i_2] < psar[i] :
                                psar[i] = self.m_lowData[i_2]
                    else :
                        if self.m_highData[i] > psar[i] :
                            isLong = 1
                            psar[i] = extremePoint
                            extremePoint = self.m_highData[i]
                            acc = accInitial
                        else :
                            if self.m_lowData[i] < extremePoint :
                                extremePoint = self.m_lowData[i]
                                acc = acc + accIncrement

                            if self.m_highData[i_1] > psar[i] :
                                psar[i] = self.m_highData[i_1]
                            if self.m_highData[i_2] > psar[i] :
                                psar[i] = self.m_highData[i_2]

                i_2 = i_1
                i_1 = i

        ret = self.addLineIndicator2(self.m_mainChart, psar, fillColor, "Parabolic SAR")
        ret.setLineWidth(0)
        ret.addDataSet(psar).setDataSymbol(symbolType, symbolSize, fillColor, edgeColor)
        return ret

    #/ <summary>
    #/ Add a comparison line to the main price chart.
    #/ </summary>
    #/ <param name="data">The data series to compare to</param>
    #/ <param name="color">The color of the comparison line</param>
    #/ <param name="name">The name of the comparison line</param>
    #/ <returns>The LineLayer object representing the line layer created.</returns>
    def addComparison(self, data, color, name) :
        firstIndex = self.m_extraPoints
        while (firstIndex < len(data)) and (firstIndex < len(self.m_closeData)) :
            if (data[firstIndex] != NoValue) and (self.m_closeData[firstIndex] != NoValue) and (
                data[firstIndex] != 0) and (self.m_closeData[firstIndex] != 0) :
                break
            firstIndex = firstIndex + 1
        if (firstIndex >= len(data)) or (firstIndex >= len(self.m_closeData)) :
            return None

        scaleFactor = self.m_closeData[firstIndex] / data[firstIndex]
        layer = self.m_mainChart.addLineLayer(ArrayMath(data).mul(scaleFactor).result(), Transparent
            )
        layer.setHTMLImageMap("{disable}")

        a = self.m_mainChart.addAxis(Right, 0)
        a.setColors(Transparent, Transparent)
        a.syncAxis(self.m_mainChart.yAxis(), 1 / scaleFactor, 0)

        ret = self.addLineIndicator2(self.m_mainChart, data, color, name)
        ret.setUseYAxis(a)
        return ret

    #/ <summary>
    #/ Display percentage axis scale
    #/ </summary>
    #/ <returns>The Axis object representing the percentage axis.</returns>
    def setPercentageAxis(self) :
        firstClose = self.firstCloseValue()
        if firstClose == NoValue :
            return None

        axisAlign = Left
        if self.m_axisOnRight :
            axisAlign = Right

        ret = self.m_mainChart.addAxis(axisAlign, 0)
        self.configureYAxis(ret, 300)
        ret.syncAxis(self.m_mainChart.yAxis(), 100 / firstClose)
        ret.setRounding(0, 0)
        ret.setLabelFormat("{={value}-100|@}%")
        self.m_mainChart.yAxis().setColors(Transparent, Transparent)
        self.m_mainChart.getPlotArea().setGridAxis(None, ret)
        return ret

    #/ <summary>
    #/ Add a generic band to the main finance chart. This method is used internally by other methods to add
    #/ various bands (eg. Bollinger band, Donchian channels, etc).
    #/ </summary>
    #/ <param name="upperLine">The data series for the upper band line.</param>
    #/ <param name="lowerLine">The data series for the lower band line.</param>
    #/ <param name="lineColor">The color of the upper and lower band line.</param>
    #/ <param name="fillColor">The color to fill the region between the upper and lower band lines.</param>
    #/ <param name="name">The name of the band.</param>
    #/ <returns>An InterLineLayer object representing the filled region.</returns>
    def addBand(self, upperLine, lowerLine, lineColor, fillColor, name) :
        i = len(upperLine) - 1
        if i >= len(lowerLine) :
            i = len(lowerLine) - 1

        while i >= 0 :
            if (upperLine[i] != NoValue) and (lowerLine[i] != NoValue) :
                name = "%s: %s - %s" % (name, self.formatValue(lowerLine[i], self.m_generalFormat),
                    self.formatValue(upperLine[i], self.m_generalFormat))
                break
            i = i - 1

        uLayer = self.m_mainChart.addLineLayer(upperLine, lineColor, name)
        lLayer = self.m_mainChart.addLineLayer(lowerLine, lineColor)
        return self.m_mainChart.addInterLineLayer(uLayer.getLine(), lLayer.getLine(), fillColor)

    #/ <summary>
    #/ Add a Bollinger band on the main chart.
    #/ </summary>
    #/ <param name="period">The period to compute the band.</param>
    #/ <param name="bandWidth">The half-width of the band in terms multiples of standard deviation. Typically 2 is used.</param>
    #/ <param name="lineColor">The color of the lines defining the upper and lower limits.</param>
    #/ <param name="fillColor">The color to fill the regional within the band.</param>
    #/ <returns>The InterLineLayer object representing the band created.</returns>
    def addBollingerBand(self, period, bandWidth, lineColor, fillColor) :
        #Bollinger Band is moving avg +/- (width * moving std deviation)
        stdDev = ArrayMath(self.m_closeData).movStdDev(period).mul(bandWidth).result()
        movAvg = ArrayMath(self.m_closeData).movAvg(period).result()
        label = "Bollinger (%s, %s)" % (period, bandWidth)
        return self.addBand(ArrayMath(movAvg).add(stdDev).result(), ArrayMath(movAvg).sub(stdDev
            ).selectGTZ(None, 0).result(), lineColor, fillColor, label)

    #/ <summary>
    #/ Add a Donchian channel on the main chart.
    #/ </summary>
    #/ <param name="period">The period to compute the band.</param>
    #/ <param name="lineColor">The color of the lines defining the upper and lower limits.</param>
    #/ <param name="fillColor">The color to fill the regional within the band.</param>
    #/ <returns>The InterLineLayer object representing the band created.</returns>
    def addDonchianChannel(self, period, lineColor, fillColor) :
        #Donchian Channel is the zone between the moving max and moving min
        label = "Donchian (%s)" % (period)
        return self.addBand(ArrayMath(self.m_highData).movMax(period).result(), ArrayMath(
            self.m_lowData).movMin(period).result(), lineColor, fillColor, label)

    #/ <summary>
    #/ Add a price envelop on the main chart. The price envelop is a defined as a ratio around a
    #/ moving average. For example, a ratio of 0.2 means 20% above and below the moving average.
    #/ </summary>
    #/ <param name="period">The period for the moving average.</param>
    #/ <param name="range">The ratio above and below the moving average.</param>
    #/ <param name="lineColor">The color of the lines defining the upper and lower limits.</param>
    #/ <param name="fillColor">The color to fill the regional within the band.</param>
    #/ <returns>The InterLineLayer object representing the band created.</returns>
    def addEnvelop(self, period, range, lineColor, fillColor) :
        #Envelop is moving avg +/- percentage
        movAvg = ArrayMath(self.m_closeData).movAvg(period).result()
        label = "Envelop (SMA %s +/- %s%%)" % (period, int(range * 100))
        return self.addBand(ArrayMath(movAvg).mul(1 + range).result(), ArrayMath(movAvg).mul(
            1 - range).result(), lineColor, fillColor, label)

    #/ <summary>
    #/ Add a volume bar chart layer on the main chart.
    #/ </summary>
    #/ <param name="height">The height of the bar chart layer in pixels.</param>
    #/ <param name="upColor">The color to used on an 'up' day. An 'up' day is a day where
    #/ the closing price is higher than that of the previous day.</param>
    #/ <param name="downColor">The color to used on a 'down' day. A 'down' day is a day
    #/ where the closing price is lower than that of the previous day.</param>
    #/ <param name="flatColor">The color to used on a 'flat' day. A 'flat' day is a day
    #/ where the closing price is the same as that of the previous day.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addVolBars(self, height, upColor, downColor, flatColor) :
        return self.addVolBars2(self.m_mainChart, height, upColor, downColor, flatColor)

    def addVolBars2(self, c, height, upColor, downColor, flatColor) :
        barLayer = c.addBarLayer2(Overlay)
        barLayer.setBorderColor(Transparent)

        if c == self.m_mainChart :
            self.configureYAxis(c.yAxis2(), height)
            topMargin = c.getDrawArea().getHeight(
                ) - self.m_topMargin - self.m_bottomMargin - height + self.m_yAxisMargin
            if topMargin < 0 :
                topMargin = 0
            c.yAxis2().setTopMargin(topMargin)
            barLayer.setUseYAxis2()

        a = c.yAxis2()
        if c != self.m_mainChart :
            a = c.yAxis()
        if ArrayMath(self.m_volData).max() < 10 :
            a.setLabelFormat("{value|1}%s" % (self.m_volUnit))
        else :
            a.setLabelFormat("{value}%s" % (self.m_volUnit))

        closeChange = ArrayMath(self.m_closeData).delta().result()
        i = self.lastIndex(self.m_volData)
        label = "Vol"
        if i >= 0 :
            label = "%s: %s%s" % (label, self.formatValue(self.m_volData[i], self.m_generalFormat),
                self.m_volUnit)
            closeChange[0] = 0

        upDS = barLayer.addDataSet(ArrayMath(self.m_volData).selectGTZ(closeChange).result(),
            upColor)
        dnDS = barLayer.addDataSet(ArrayMath(self.m_volData).selectLTZ(closeChange).result(),
            downColor)
        flatDS = barLayer.addDataSet(ArrayMath(self.m_volData).selectEQZ(closeChange).result(),
            flatColor)

        if (i < 0) or (closeChange[i] == 0) or (closeChange[i] == NoValue) :
            flatDS.setDataName(label)
        elif closeChange[i] > 0 :
            upDS.setDataName(label)
        else :
            dnDS.setDataName(label)

        return barLayer

    #/ <summary>
    #/ Add a blank indicator chart to the finance chart. Used internally to add other indicators.
    #/ Override to change the default formatting (eg. axis fonts, etc.) of the various indicators.
    #/ </summary>
    #/ <param name="height">The height of the chart in pixels.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addIndicator(self, height) :
        #create a new chart object
        ret = XYChart(self.m_totalWidth, height + self.m_topMargin + self.m_bottomMargin,
            Transparent)
        ret.setTrimData(self.m_extraPoints)

        if self.m_currentChart != None :
            #if there is a chart before the newly created chart, disable its x-axis, and copy
            #its x-axis labels to the new chart
            self.m_currentChart.xAxis().setColors(Transparent, Transparent)
            ret.xAxis().copyAxis(self.m_currentChart.xAxis())

            #add chart to MultiChart and update the total height
            self.addChart(0, self.m_totalHeight + self.m_plotAreaGap, ret)
            self.m_totalHeight = self.m_totalHeight + height + 1 + self.m_plotAreaGap
        else :
            #no existing chart - create the x-axis labels from scratch
            self.setXLabels(ret.xAxis())

            #add chart to MultiChart and update the total height
            self.addChart(0, self.m_totalHeight, ret)
            self.m_totalHeight = self.m_totalHeight + height + 1

        #the newly created chart becomes the current chart
        self.m_currentChart = ret

        #update the size
        self.setSize(self.m_totalWidth, self.m_totalHeight + self.m_topMargin + self.m_bottomMargin)

        #configure the plot area
        ret.setPlotArea(self.m_leftMargin, self.m_topMargin,
            self.m_totalWidth - self.m_leftMargin - self.m_rightMargin, height,
            self.m_plotAreaBgColor, -1, self.m_plotAreaBorder).setGridColor(self.m_majorHGridColor,
            self.m_majorVGridColor, self.m_minorHGridColor, self.m_minorVGridColor)
        ret.setAntiAlias(self.m_antiAlias)

        #configure legend box
        box = ret.addLegend(self.m_leftMargin, self.m_topMargin, 0, self.m_legendFont,
            self.m_legendFontSize)
        box.setFontColor(self.m_legendFontColor)
        box.setBackground(self.m_legendBgColor)
        box.setMargin2(5, 0, 2, 1)
        box.setSize(self.m_totalWidth - self.m_leftMargin - self.m_rightMargin + 1, 0)

        #configure x-axis
        a = ret.xAxis()
        a.setIndent(1)
        a.setTickLength(2, 0)
        a.setColors(Transparent, self.m_xAxisFontColor, self.m_xAxisFontColor, self.m_xAxisFontColor
            )
        a.setLabelStyle(self.m_xAxisFont, self.m_xAxisFontSize, self.m_xAxisFontColor,
            self.m_xAxisFontAngle)

        #configure y-axis
        ret.setYAxisOnRight(self.m_axisOnRight)
        self.configureYAxis(ret.yAxis(), height)

        return ret

    def configureYAxis(self, a, height) :
        a.setAutoScale(0, 0.05, 0)
        if height < 100 :
            a.setTickDensity(15)
        a.setMargin(self.m_yAxisMargin)
        a.setLabelStyle(self.m_yAxisFont, self.m_yAxisFontSize, self.m_yAxisFontColor, 0)
        a.setTickLength(-4, -2)
        a.setColors(Transparent, self.m_yAxisFontColor, self.m_yAxisFontColor, self.m_yAxisFontColor
            )

    #/ <summary>
    #/ Add a generic line indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="data">The data series of the indicator line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="name">The name of the indicator.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addLineIndicator(self, height, data, color, name) :
        c = self.addIndicator(height)
        self.addLineIndicator2(c, data, color, name)
        return c

    #/ <summary>
    #/ Add a line to an existing indicator chart.
    #/ </summary>
    #/ <param name="c">The indicator chart to add the line to.</param>
    #/ <param name="data">The data series of the indicator line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="name">The name of the indicator.</param>
    #/ <returns>The LineLayer object representing the line created.</returns>
    def addLineIndicator2(self, c, data, color, name) :
        return c.addLineLayer(data, color, self.formatIndicatorLabel(name, data))

    #/ <summary>
    #/ Add a generic bar indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="data">The data series of the indicator bars.</param>
    #/ <param name="color">The color of the indicator bars.</param>
    #/ <param name="name">The name of the indicator.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addBarIndicator(self, height, data, color, name) :
        c = self.addIndicator(height)
        self.addBarIndicator2(c, data, color, name)
        return c

    #/ <summary>
    #/ Add a bar layer to an existing indicator chart.
    #/ </summary>
    #/ <param name="c">The indicator chart to add the bar layer to.</param>
    #/ <param name="data">The data series of the indicator bars.</param>
    #/ <param name="color">The color of the indicator bars.</param>
    #/ <param name="name">The name of the indicator.</param>
    #/ <returns>The BarLayer object representing the bar layer created.</returns>
    def addBarIndicator2(self, c, data, color, name) :
        layer = c.addBarLayer(data, color, self.formatIndicatorLabel(name, data))
        layer.setBorderColor(Transparent)
        return layer

    #/ <summary>
    #/ Add an upper/lower threshold range to an existing indicator chart.
    #/ </summary>
    #/ <param name="c">The indicator chart to add the threshold range to.</param>
    #/ <param name="layer">The line layer that the threshold range applies to.</param>
    #/ <param name="topRange">The upper threshold.</param>
    #/ <param name="topColor">The color to fill the region of the line that is above the
    #/ upper threshold.</param>
    #/ <param name="bottomRange">The lower threshold.</param>
    #/ <param name="bottomColor">The color to fill the region of the line that is below
    #/ the lower threshold.</param>
    def addThreshold(self, c, layer, topRange, topColor, bottomRange, bottomColor) :
        topMark = c.yAxis().addMark(topRange, topColor, self.formatValue(topRange,
            self.m_generalFormat))
        bottomMark = c.yAxis().addMark(bottomRange, bottomColor, self.formatValue(bottomRange,
            self.m_generalFormat))

        c.addInterLineLayer(layer.getLine(), topMark.getLine(), topColor, Transparent)
        c.addInterLineLayer(layer.getLine(), bottomMark.getLine(), Transparent, bottomColor)

    def formatIndicatorLabel(self, name, data) :
        i = self.lastIndex(data)
        if name == None :
            return name
        if (name == "") or (i < 0) :
            return name
        ret = "%s: %s" % (name, self.formatValue(data[i], self.m_generalFormat))
        return ret

    #/ <summary>
    #/ Add an Accumulation/Distribution indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addAccDist(self, height, color) :
        #Close Location Value = ((C - L) - (H - C)) / (H - L)
        #Accumulation Distribution Line = Accumulation of CLV * volume
        range = ArrayMath(self.m_highData).sub(self.m_lowData).result()
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).mul(2).sub(self.m_lowData
            ).sub(self.m_highData).mul(self.m_volData).financeDiv(range, 0).acc().result(), color,
            "Accumulation/Distribution")

    def computeAroonUp(self, period) :
        aroonUp = [0] * len(self.m_highData)
        for i in range(0, len(self.m_highData)) :
            highValue = self.m_highData[i]
            if highValue == NoValue :
                aroonUp[i] = NoValue
            else :
                currentIndex = i
                highCount = period
                count = period

                while (count > 0) and (currentIndex >= count) :
                    currentIndex = currentIndex - 1
                    currentValue = self.m_highData[currentIndex]
                    if currentValue != NoValue :
                        count = count - 1
                        if currentValue > highValue :
                            highValue = currentValue
                            highCount = count

                if count > 0 :
                    aroonUp[i] = NoValue
                else :
                    aroonUp[i] = highCount * 100.0 / period

        return aroonUp

    def computeAroonDn(self, period) :
        aroonDn = [0] * len(self.m_lowData)
        for i in range(0, len(self.m_lowData)) :
            lowValue = self.m_lowData[i]
            if lowValue == NoValue :
                aroonDn[i] = NoValue
            else :
                currentIndex = i
                lowCount = period
                count = period

                while (count > 0) and (currentIndex >= count) :
                    currentIndex = currentIndex - 1
                    currentValue = self.m_lowData[currentIndex]
                    if currentValue != NoValue :
                        count = count - 1
                        if currentValue < lowValue :
                            lowValue = currentValue
                            lowCount = count

                if count > 0 :
                    aroonDn[i] = NoValue
                else :
                    aroonDn[i] = lowCount * 100.0 / period

        return aroonDn

    #/ <summary>
    #/ Add an Aroon Up/Down indicators chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicators.</param>
    #/ <param name="upColor">The color of the Aroon Up indicator line.</param>
    #/ <param name="downColor">The color of the Aroon Down indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addAroon(self, height, period, upColor, downColor) :
        c = self.addIndicator(height)
        self.addLineIndicator2(c, self.computeAroonUp(period), upColor, "Aroon Up")
        self.addLineIndicator2(c, self.computeAroonDn(period), downColor, "Aroon Down")
        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add an Aroon Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addAroonOsc(self, height, period, color) :
        label = "Aroon Oscillator (%s)" % (period)
        c = self.addLineIndicator(height, ArrayMath(self.computeAroonUp(period)).sub(
            self.computeAroonDn(period)).result(), color, label)
        c.yAxis().setLinearScale(-100, 100)
        return c

    def computeTrueRange(self) :
        previousClose = ArrayMath(self.m_closeData).shift().result()
        ret = ArrayMath(self.m_highData).sub(self.m_lowData).result()
        temp = 0

        for i in range(0, len(self.m_highData)) :
            if (ret[i] != NoValue) and (previousClose[i] != NoValue) :
                temp = abs(self.m_highData[i] - previousClose[i])
                if temp > ret[i] :
                    ret[i] = temp
                temp = abs(previousClose[i] - self.m_lowData[i])
                if temp > ret[i] :
                    ret[i] = temp

        return ret

    #/ <summary>
    #/ Add an Average Directional Index indicators chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="posColor">The color of the Positive Directional Index line.</param>
    #/ <param name="negColor">The color of the Negatuve Directional Index line.</param>
    #/ <param name="color">The color of the Average Directional Index line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addADX(self, height, period, posColor, negColor, color) :
        #pos/neg directional movement
        pos = ArrayMath(self.m_highData).delta().selectGTZ()
        neg = ArrayMath(self.m_lowData).delta().mul(-1).selectGTZ()
        delta = ArrayMath(pos.result()).sub(neg.result()).result()
        pos.selectGTZ(delta)
        neg.selectLTZ(delta)

        #pos/neg directional index
        tr = self.computeTrueRange()
        pos.financeDiv(tr, 0.25).mul(100).expAvg(2.0 / (period + 1))
        neg.financeDiv(tr, 0.25).mul(100).expAvg(2.0 / (period + 1))

        #directional movement index ??? what happen if division by zero???
        totalDM = ArrayMath(pos.result()).add(neg.result()).result()
        dx = ArrayMath(pos.result()).sub(neg.result()).abs().financeDiv(totalDM, 0).mul(100).expAvg(
            2.0 / (period + 1))

        c = self.addIndicator(height)
        label1 = "+DI (%s)" % (period)
        label2 = "-DI (%s)" % (period)
        label3 = "ADX (%s)" % (period)
        self.addLineIndicator2(c, pos.result(), posColor, label1)
        self.addLineIndicator2(c, neg.result(), negColor, label2)
        self.addLineIndicator2(c, dx.result(), color, label3)
        return c

    #/ <summary>
    #/ Add an Average True Range indicators chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color1">The color of the True Range line.</param>
    #/ <param name="color2">The color of the Average True Range line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addATR(self, height, period, color1, color2) :
        trueRange = self.computeTrueRange()
        c = self.addLineIndicator(height, trueRange, color1, "True Range")
        label = "Average True Range (%s)" % (period)
        self.addLineIndicator2(c, ArrayMath(trueRange).expAvg(2.0 / (period + 1)).result(), color2,
            label)
        return c

    #/ <summary>
    #/ Add a Bollinger Band Width indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="width">The band width to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addBollingerWidth(self, height, period, width, color) :
        label = "Bollinger Width (%s, %s)" % (period, width)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).movStdDev(period).mul(
            width * 2).result(), color, label)

    #/ <summary>
    #/ Add a Community Channel Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addCCI(self, height, period, color, range, upColor, downColor) :
        #typical price
        tp = ArrayMath(self.m_highData).add(self.m_lowData).add(self.m_closeData).div(3).result()

        #simple moving average of typical price
        smvtp = ArrayMath(tp).movAvg(period).result()

        #compute mean deviation
        movMeanDev = [0] * len(smvtp)
        for i in range(0, len(smvtp)) :
            avg = smvtp[i]
            if avg == NoValue :
                movMeanDev[i] = NoValue
            else :
                currentIndex = i
                count = period - 1
                acc = 0

                while (count > 0) and (currentIndex >= count) :
                    currentIndex = currentIndex - 1
                    currentValue = tp[currentIndex]
                    if currentValue != NoValue :
                        count = count - 1
                        acc = acc + abs(avg - currentValue)

                if count > 0 :
                    movMeanDev[i] = NoValue
                else :
                    movMeanDev[i] = acc / period

        c = self.addIndicator(height)
        label = "CCI (%s)" % (period)
        layer = self.addLineIndicator2(c, ArrayMath(tp).sub(smvtp).financeDiv(movMeanDev, 0).div(
            0.015).result(), color, label)
        self.addThreshold(c, layer, range, upColor,  - range, downColor)
        return c

    #/ <summary>
    #/ Add a Chaikin Money Flow indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addChaikinMoneyFlow(self, height, period, color) :
        range = ArrayMath(self.m_highData).sub(self.m_lowData).result()
        volAvg = ArrayMath(self.m_volData).movAvg(period).result()
        label = "Chaikin Money Flow (%s)" % (period)
        return self.addBarIndicator(height, ArrayMath(self.m_closeData).mul(2).sub(self.m_lowData
            ).sub(self.m_highData).mul(self.m_volData).financeDiv(range, 0).movAvg(period
            ).financeDiv(volAvg, 0).result(), color, label)

    #/ <summary>
    #/ Add a Chaikin Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addChaikinOscillator(self, height, color) :
        #first compute acc/dist line
        range = ArrayMath(self.m_highData).sub(self.m_lowData).result()
        accdist = ArrayMath(self.m_closeData).mul(2).sub(self.m_lowData).sub(self.m_highData).mul(
            self.m_volData).financeDiv(range, 0).acc().result()

        #chaikin osc = exp3(accdist) - exp10(accdist)
        expAvg10 = ArrayMath(accdist).expAvg(2.0 / (10 + 1)).result()
        return self.addLineIndicator(height, ArrayMath(accdist).expAvg(2.0 / (3 + 1)).sub(expAvg10
            ).result(), color, "Chaikin Oscillator")

    #/ <summary>
    #/ Add a Chaikin Volatility indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The period to smooth the range.</param>
    #/ <param name="period2">The period to compute the rate of change of the smoothed range.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addChaikinVolatility(self, height, period1, period2, color) :
        label = "Chaikin Volatility (%s, %s)" % (period1, period2)
        return self.addLineIndicator(height, ArrayMath(self.m_highData).sub(self.m_lowData).expAvg(
            2.0 / (period1 + 1)).rate(period2).sub(1).mul(100).result(), color, label)

    #/ <summary>
    #/ Add a Close Location Value indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addCLV(self, height, color) :
        #Close Location Value = ((C - L) - (H - C)) / (H - L)
        range = ArrayMath(self.m_highData).sub(self.m_lowData).result()
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).mul(2).sub(self.m_lowData
            ).sub(self.m_highData).financeDiv(range, 0).result(), color, "Close Location Value")

    #/ <summary>
    #/ Add a Detrended Price Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addDPO(self, height, period, color) :
        label = "DPO (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).movAvg(period).shift(
            period / 2 + 1).sub(self.m_closeData).mul(-1).result(), color, label)

    #/ <summary>
    #/ Add a Donchian Channel Width indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addDonchianWidth(self, height, period, color) :
        label = "Donchian Width (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_highData).movMax(period).sub(
            ArrayMath(self.m_lowData).movMin(period).result()).result(), color, label)

    #/ <summary>
    #/ Add a Ease of Movement indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to smooth the indicator.</param>
    #/ <param name="color1">The color of the indicator line.</param>
    #/ <param name="color2">The color of the smoothed indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addEaseOfMovement(self, height, period, color1, color2) :
        boxRatioInverted = ArrayMath(self.m_highData).sub(self.m_lowData).financeDiv(self.m_volData,
            0).result()
        result = ArrayMath(self.m_highData).add(self.m_lowData).div(2).delta().mul(boxRatioInverted
            ).result()

        c = self.addLineIndicator(height, result, color1, "EMV")
        label = "EMV EMA (%s)" % (period)
        self.addLineIndicator2(c, ArrayMath(result).movAvg(period).result(), color2, label)
        return c

    #/ <summary>
    #/ Add a Fast Stochastic indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The period to compute the %K line.</param>
    #/ <param name="period2">The period to compute the %D line.</param>
    #/ <param name="color1">The color of the %K line.</param>
    #/ <param name="color2">The color of the %D line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addFastStochastic(self, height, period1, period2, color1, color2) :
        movLow = ArrayMath(self.m_lowData).movMin(period1).result()
        movRange = ArrayMath(self.m_highData).movMax(period1).sub(movLow).result()
        stochastic = ArrayMath(self.m_closeData).sub(movLow).financeDiv(movRange, 0.5).mul(100
            ).result()

        label1 = "Fast Stochastic %%K (%s)" % (period1)
        c = self.addLineIndicator(height, stochastic, color1, label1)
        label2 = "%%D (%s)" % (period2)
        self.addLineIndicator2(c, ArrayMath(stochastic).movAvg(period2).result(), color2, label2)

        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a MACD indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The first moving average period to compute the indicator.</param>
    #/ <param name="period2">The second moving average period to compute the indicator.</param>
    #/ <param name="period3">The moving average period of the signal line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="signalColor">The color of the signal line.</param>
    #/ <param name="divColor">The color of the divergent bars.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addMACD(self, height, period1, period2, period3, color, signalColor, divColor) :
        c = self.addIndicator(height)

        #MACD is defined as the difference between two exponential averages (typically 12/26 days)
        expAvg1 = ArrayMath(self.m_closeData).expAvg(2.0 / (period1 + 1)).result()
        macd = ArrayMath(self.m_closeData).expAvg(2.0 / (period2 + 1)).sub(expAvg1).result()

        #Add the MACD line
        label1 = "MACD (%s, %s)" % (period1, period2)
        self.addLineIndicator2(c, macd, color, label1)

        #MACD signal line
        macdSignal = ArrayMath(macd).expAvg(2.0 / (period3 + 1)).result()
        label2 = "EXP (%s)" % (period3)
        self.addLineIndicator2(c, macdSignal, signalColor, label2)

        #Divergence
        self.addBarIndicator2(c, ArrayMath(macd).sub(macdSignal).result(), divColor, "Divergence")

        return c

    #/ <summary>
    #/ Add a Mass Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addMassIndex(self, height, color, upColor, downColor) :
        #Mass Index
        f = 2.0 / (10)
        exp9 = ArrayMath(self.m_highData).sub(self.m_lowData).expAvg(f).result()
        exp99 = ArrayMath(exp9).expAvg(f).result()

        c = self.addLineIndicator(height, ArrayMath(exp9).financeDiv(exp99, 1).movAvg(25).mul(25
            ).result(), color, "Mass Index")
        c.yAxis().addMark(27, upColor)
        c.yAxis().addMark(26.5, downColor)
        return c

    #/ <summary>
    #/ Add a Money Flow Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addMFI(self, height, period, color, range, upColor, downColor) :
        #Money Flow Index
        typicalPrice = ArrayMath(self.m_highData).add(self.m_lowData).add(self.m_closeData).div(3
            ).result()
        moneyFlow = ArrayMath(typicalPrice).mul(self.m_volData).result()

        selector = ArrayMath(typicalPrice).delta().result()
        posMoneyFlow = ArrayMath(moneyFlow).selectGTZ(selector).movAvg(period).result()
        posNegMoneyFlow = ArrayMath(moneyFlow).selectLTZ(selector).movAvg(period).add(posMoneyFlow
            ).result()

        c = self.addIndicator(height)
        label = "Money Flow Index (%s)" % (period)
        layer = self.addLineIndicator2(c, ArrayMath(posMoneyFlow).financeDiv(posNegMoneyFlow, 0.5
            ).mul(100).result(), color, label)
        self.addThreshold(c, layer, 50 + range, upColor, 50 - range, downColor)

        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a Momentum indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addMomentum(self, height, period, color) :
        label = "Momentum (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).delta(period).result(),
            color, label)

    #/ <summary>
    #/ Add a Negative Volume Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the signal line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="signalColor">The color of the signal line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addNVI(self, height, period, color, signalColor) :
        nvi = [0] * len(self.m_volData)

        previousNVI = 100
        previousVol = NoValue
        previousClose = NoValue
        for i in range(0, len(self.m_volData)) :
            if self.m_volData[i] == NoValue :
                nvi[i] = NoValue
            else :
                if (previousVol != NoValue) and (self.m_volData[i] < previousVol) and (
                    previousClose != NoValue) and (self.m_closeData[i] != NoValue) :
                    nvi[i] = previousNVI + previousNVI * (self.m_closeData[i] - previousClose
                        ) / previousClose
                else :
                    nvi[i] = previousNVI

                previousNVI = nvi[i]
                previousVol = self.m_volData[i]
                previousClose = self.m_closeData[i]

        c = self.addLineIndicator(height, nvi, color, "NVI")
        if len(nvi) > period :
            label = "NVI SMA (%s)" % (period)
            self.addLineIndicator2(c, ArrayMath(nvi).movAvg(period).result(), signalColor, label)
        return c

    #/ <summary>
    #/ Add an On Balance Volume indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addOBV(self, height, color) :
        closeChange = ArrayMath(self.m_closeData).delta().result()
        upVolume = ArrayMath(self.m_volData).selectGTZ(closeChange).result()
        downVolume = ArrayMath(self.m_volData).selectLTZ(closeChange).result()

        return self.addLineIndicator(height, ArrayMath(upVolume).sub(downVolume).acc().result(),
            color, "OBV")

    #/ <summary>
    #/ Add a Performance indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addPerformance(self, height, color) :
        closeValue = self.firstCloseValue()
        if closeValue != NoValue :
            return self.addLineIndicator(height, ArrayMath(self.m_closeData).mul(100 / closeValue
                ).sub(100).result(), color, "Performance")
        else :
            #chart is empty !!!
            return self.addIndicator(height)

    #/ <summary>
    #/ Add a Percentage Price Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The first moving average period to compute the indicator.</param>
    #/ <param name="period2">The second moving average period to compute the indicator.</param>
    #/ <param name="period3">The moving average period of the signal line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="signalColor">The color of the signal line.</param>
    #/ <param name="divColor">The color of the divergent bars.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addPPO(self, height, period1, period2, period3, color, signalColor, divColor) :
        expAvg1 = ArrayMath(self.m_closeData).expAvg(2.0 / (period1 + 1)).result()
        expAvg2 = ArrayMath(self.m_closeData).expAvg(2.0 / (period2 + 1)).result()
        ppo = ArrayMath(expAvg2).sub(expAvg1).financeDiv(expAvg2, 0).mul(100)
        ppoSignal = ArrayMath(ppo.result()).expAvg(2.0 / (period3 + 1)).result()

        label1 = "PPO (%s, %s)" % (period1, period2)
        label2 = "EMA (%s)" % (period3)
        c = self.addLineIndicator(height, ppo.result(), color, label1)
        self.addLineIndicator2(c, ppoSignal, signalColor, label2)
        self.addBarIndicator2(c, ppo.sub(ppoSignal).result(), divColor, "Divergence")
        return c

    #/ <summary>
    #/ Add a Positive Volume Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the signal line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="signalColor">The color of the signal line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addPVI(self, height, period, color, signalColor) :
        #Positive Volume Index
        pvi = [0] * len(self.m_volData)

        previousPVI = 100
        previousVol = NoValue
        previousClose = NoValue
        for i in range(0, len(self.m_volData)) :
            if self.m_volData[i] == NoValue :
                pvi[i] = NoValue
            else :
                if (previousVol != NoValue) and (self.m_volData[i] > previousVol) and (
                    previousClose != NoValue) and (self.m_closeData[i] != NoValue) :
                    pvi[i] = previousPVI + previousPVI * (self.m_closeData[i] - previousClose
                        ) / previousClose
                else :
                    pvi[i] = previousPVI

                previousPVI = pvi[i]
                previousVol = self.m_volData[i]
                previousClose = self.m_closeData[i]

        c = self.addLineIndicator(height, pvi, color, "PVI")
        if len(pvi) > period :
            label = "PVI SMA (%s)" % (period)
            self.addLineIndicator2(c, ArrayMath(pvi).movAvg(period).result(), signalColor, label)
        return c

    #/ <summary>
    #/ Add a Percentage Volume Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The first moving average period to compute the indicator.</param>
    #/ <param name="period2">The second moving average period to compute the indicator.</param>
    #/ <param name="period3">The moving average period of the signal line.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="signalColor">The color of the signal line.</param>
    #/ <param name="divColor">The color of the divergent bars.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addPVO(self, height, period1, period2, period3, color, signalColor, divColor) :
        expAvg1 = ArrayMath(self.m_volData).expAvg(2.0 / (period1 + 1)).result()
        expAvg2 = ArrayMath(self.m_volData).expAvg(2.0 / (period2 + 1)).result()
        pvo = ArrayMath(expAvg2).sub(expAvg1).financeDiv(expAvg2, 0).mul(100)
        pvoSignal = ArrayMath(pvo.result()).expAvg(2.0 / (period3 + 1)).result()

        label1 = "PVO (%s, %s)" % (period1, period2)
        label2 = "EMA (%s)" % (period3)
        c = self.addLineIndicator(height, pvo.result(), color, label1)
        self.addLineIndicator2(c, pvoSignal, signalColor, label2)
        self.addBarIndicator2(c, pvo.sub(pvoSignal).result(), divColor, "Divergence")
        return c

    #/ <summary>
    #/ Add a Price Volumne Trend indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addPVT(self, height, color) :
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).rate().sub(1).mul(
            self.m_volData).acc().result(), color, "PVT")

    #/ <summary>
    #/ Add a Rate of Change indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addROC(self, height, period, color) :
        label = "ROC (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).rate(period).sub(1).mul(100
            ).result(), color, label)

    def RSIMovAvg(self, data, period) :
        #The "moving average" in classical RSI is based on a formula that mixes simple
        #and exponential moving averages.

        if period <= 0 :
            period = 1

        count = 0
        acc = 0

        for i in range(0, len(data)) :
            if abs(data[i] / NoValue - 1) > 1e-005 :
                count = count + 1
                acc = acc + data[i]
                if count < period :
                    data[i] = NoValue
                else :
                    data[i] = acc / period
                    acc = data[i] * (period - 1)

        return data

    def computeRSI(self, period) :
        #RSI is defined as the average up changes for the last 14 days, divided by the
        #average absolute changes for the last 14 days, expressed as a percentage.

        absChange = self.RSIMovAvg(ArrayMath(self.m_closeData).delta().abs().result(), period)
        absUpChange = self.RSIMovAvg(ArrayMath(self.m_closeData).delta().selectGTZ().result(),
            period)
        return ArrayMath(absUpChange).financeDiv(absChange, 0.5).mul(100).result()

    #/ <summary>
    #/ Add a Relative Strength Index indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addRSI(self, height, period, color, range, upColor, downColor) :
        c = self.addIndicator(height)
        label = "RSI (%s)" % (period)
        layer = self.addLineIndicator2(c, self.computeRSI(period), color, label)

        #Add range if given
        if (range > 0) and (range < 50) :
            self.addThreshold(c, layer, 50 + range, upColor, 50 - range, downColor)
        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a Slow Stochastic indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The period to compute the %K line.</param>
    #/ <param name="period2">The period to compute the %D line.</param>
    #/ <param name="color1">The color of the %K line.</param>
    #/ <param name="color2">The color of the %D line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addSlowStochastic(self, height, period1, period2, color1, color2) :
        movLow = ArrayMath(self.m_lowData).movMin(period1).result()
        movRange = ArrayMath(self.m_highData).movMax(period1).sub(movLow).result()
        stochastic = ArrayMath(self.m_closeData).sub(movLow).financeDiv(movRange, 0.5).mul(100
            ).movAvg(3)

        label1 = "Slow Stochastic %%K (%s)" % (period1)
        label2 = "%%D (%s)" % (period2)
        c = self.addLineIndicator(height, stochastic.result(), color1, label1)
        self.addLineIndicator2(c, stochastic.movAvg(period2).result(), color2, label2)

        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a Moving Standard Deviation indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addStdDev(self, height, period, color) :
        label = "Moving StdDev (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).movStdDev(period).result(),
            color, label)

    #/ <summary>
    #/ Add a Stochastic RSI indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addStochRSI(self, height, period, color, range, upColor, downColor) :
        rsi = self.computeRSI(period)
        movLow = ArrayMath(rsi).movMin(period).result()
        movRange = ArrayMath(rsi).movMax(period).sub(movLow).result()

        c = self.addIndicator(height)
        label = "StochRSI (%s)" % (period)
        layer = self.addLineIndicator2(c, ArrayMath(rsi).sub(movLow).financeDiv(movRange, 0.5).mul(
            100).result(), color, label)

        #Add range if given
        if (range > 0) and (range < 50) :
            self.addThreshold(c, layer, 50 + range, upColor, 50 - range, downColor)
        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a TRIX indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addTRIX(self, height, period, color) :
        f = 2.0 / (period + 1)
        label = "TRIX (%s)" % (period)
        return self.addLineIndicator(height, ArrayMath(self.m_closeData).expAvg(f).expAvg(f).expAvg(
            f).rate().sub(1).mul(100).result(), color, label)

    def computeTrueLow(self) :
        #the lower of today's low or yesterday's close.
        previousClose = ArrayMath(self.m_closeData).shift().result()
        ret = [0] * len(self.m_lowData)
        for i in range(0, len(self.m_lowData)) :
            if (self.m_lowData[i] != NoValue) and (previousClose[i] != NoValue) :
                if self.m_lowData[i] < previousClose[i] :
                    ret[i] = self.m_lowData[i]
                else :
                    ret[i] = previousClose[i]
            else :
                ret[i] = NoValue

        return ret

    #/ <summary>
    #/ Add an Ultimate Oscillator indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period1">The first moving average period to compute the indicator.</param>
    #/ <param name="period2">The second moving average period to compute the indicator.</param>
    #/ <param name="period3">The third moving average period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addUltimateOscillator(self, height, period1, period2, period3, color, range, upColor,
        downColor) :
        trueLow = self.computeTrueLow()
        buyingPressure = ArrayMath(self.m_closeData).sub(trueLow).result()
        trueRange = self.computeTrueRange()

        rawUO1 = ArrayMath(buyingPressure).movAvg(period1).financeDiv(ArrayMath(trueRange).movAvg(
            period1).result(), 0.5).mul(4).result()
        rawUO2 = ArrayMath(buyingPressure).movAvg(period2).financeDiv(ArrayMath(trueRange).movAvg(
            period2).result(), 0.5).mul(2).result()
        rawUO3 = ArrayMath(buyingPressure).movAvg(period3).financeDiv(ArrayMath(trueRange).movAvg(
            period3).result(), 0.5).mul(1).result()

        c = self.addIndicator(height)
        label = "Ultimate Oscillator (%s, %s, %s)" % (period1, period2, period3)
        layer = self.addLineIndicator2(c, ArrayMath(rawUO1).add(rawUO2).add(rawUO3).mul(100.0 / 7
            ).result(), color, label)
        self.addThreshold(c, layer, 50 + range, upColor, 50 - range, downColor)

        c.yAxis().setLinearScale(0, 100)
        return c

    #/ <summary>
    #/ Add a Volume indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="upColor">The color to used on an 'up' day. An 'up' day is a day where
    #/ the closing price is higher than that of the previous day.</param>
    #/ <param name="downColor">The color to used on a 'down' day. A 'down' day is a day
    #/ where the closing price is lower than that of the previous day.</param>
    #/ <param name="flatColor">The color to used on a 'flat' day. A 'flat' day is a day
    #/ where the closing price is the same as that of the previous day.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addVolIndicator(self, height, upColor, downColor, flatColor) :
        c = self.addIndicator(height)
        self.addVolBars2(c, height, upColor, downColor, flatColor)
        return c

    #/ <summary>
    #/ Add a William %R indicator chart.
    #/ </summary>
    #/ <param name="height">The height of the indicator chart in pixels.</param>
    #/ <param name="period">The period to compute the indicator.</param>
    #/ <param name="color">The color of the indicator line.</param>
    #/ <param name="range">The distance beween the middle line and the upper and lower threshold lines.</param>
    #/ <param name="upColor">The fill color when the indicator exceeds the upper threshold line.</param>
    #/ <param name="downColor">The fill color when the indicator falls below the lower threshold line.</param>
    #/ <returns>The XYChart object representing the chart created.</returns>
    def addWilliamR(self, height, period, color, range, upColor, downColor) :
        movLow = ArrayMath(self.m_lowData).movMin(period).result()
        movHigh = ArrayMath(self.m_highData).movMax(period).result()
        movRange = ArrayMath(movHigh).sub(movLow).result()

        c = self.addIndicator(height)
        layer = self.addLineIndicator2(c, ArrayMath(movHigh).sub(self.m_closeData).financeDiv(
            movRange, 0.5).mul(-100).result(), color, "William %R")
        self.addThreshold(c, layer, -50 + range, upColor, -50 - range, downColor)
        c.yAxis().setLinearScale(-100, 0)
        return c
