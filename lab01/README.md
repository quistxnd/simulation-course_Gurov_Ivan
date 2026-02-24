## Лабораторная работа №1
# Моделирование полёта тела в атмосфере
**Выполнил:** Студент группы 932302 Акрамов Темирлан  

## 1. Задание

Реализовать приложение для моделирования полёта тела в атмосфере. Предусмотреть возможность ввода шага моделирования и вывода результатов. Выполнить моделирование без очистки предыдущих результатов для различных шагов моделирования, сравнить траектории и заполнить таблицу.

## 2. Код программы

```csharp
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace lab1
{
    public partial class Form1 : Form
    {
        private const double g = 9.81;
        private const double airDensity = 1.225;
        private const double dragCoefficient = 0.47;
        private int trajectoryCounter = 0;
        private Random random = new Random();
        private System.Windows.Forms.Timer animationTimer;
        private List<PointF> animationPoints;
        private int currentPointIndex;
        private Series activeSeries;

        public Form1()
        {
            InitializeComponent();
            SetupChart();
            SetupGrid();

            animationTimer = new System.Windows.Forms.Timer { Interval = 50 };
            animationTimer.Tick += AnimationTimer_Tick;
        }

        private void SetupChart()
        {
            var chartArea = chartTrajectory.ChartAreas[0];
            chartArea.AxisX.Title = "Дальность, м";
            chartArea.AxisY.Title = "Высота, м";
            chartArea.AxisX.MajorGrid.Enabled = true;
            chartArea.AxisY.MajorGrid.Enabled = true;
            chartArea.AxisX.Interval = 20;
            chartArea.AxisY.Interval = 4;
            chartArea.AxisX.LabelStyle.Format = "F0";
            chartArea.AxisY.LabelStyle.Format = "F0";

            chartTrajectory.Series.Clear();
            chartTrajectory.Legends.Clear();
            Legend legend = new Legend("MainLegend");
            legend.Docking = Docking.Bottom;
            legend.Alignment = StringAlignment.Center;
            legend.Font = new Font("Segoe UI", 9);
            chartTrajectory.Legends.Add(legend);
        }

        private void SetupGrid()
        {
            dataGridViewResults.Columns.Clear();
            dataGridViewResults.Columns.Add("Step", "Шаг моделирования, с");
            dataGridViewResults.Columns.Add("Range", "Дальность полёта, м");
            dataGridViewResults.Columns.Add("Height", "Максимальная высота, м");
            dataGridViewResults.Columns.Add("Speed", "Скорость в конечной точке, м/с");
        }

        private class SimulationResult
        {
            public double Range { get; set; }
            public double MaxHeight { get; set; }
            public double FinalSpeed { get; set; }
            public List<PointF> Points { get; set; }
        }

        private class State
        {
            public double X { get; set; }
            public double Y { get; set; }
            public double Vx { get; set; }
            public double Vy { get; set; }
        }

        private State GetDerivatives(State s, double mass, double area)
        {
            double v = Math.Sqrt(s.Vx * s.Vx + s.Vy * s.Vy);
            double dragForce = 0.5 * dragCoefficient * airDensity * v * v * area;

            double ax = (v > 0) ? -dragForce * s.Vx / v / mass : 0;
            double ay = -g + ((v > 0) ? -dragForce * s.Vy / v / mass : 0);

            return new State
            {
                X = s.Vx,
                Y = s.Vy,
                Vx = ax,
                Vy = ay
            };
        }

        private SimulationResult Simulate(double dt)
        {
            double h0 = (double)numInitHeight.Value;
            double v0 = (double)numVelocity.Value;
            double angle = (double)numAngle.Value * Math.PI / 180.0;
            double mass = (double)numMass.Value;
            double diameter = (double)numDiameter.Value;

            State s = new State
            {
                X = 0,
                Y = h0,
                Vx = v0 * Math.Cos(angle),
                Vy = v0 * Math.Sin(angle)
            };

            double maxY = h0;
            List<PointF> points = new List<PointF>();
            points.Add(new PointF((float)s.X, (float)s.Y));

            double area = Math.PI * Math.Pow(diameter / 2.0, 2);

            while (s.Y >= 0)
            {
                State k1 = GetDerivatives(s, mass, area);

                State s2 = new State
                {
                    X = s.X + k1.X * dt * 0.5,
                    Y = s.Y + k1.Y * dt * 0.5,
                    Vx = s.Vx + k1.Vx * dt * 0.5,
                    Vy = s.Vy + k1.Vy * dt * 0.5
                };
                State k2 = GetDerivatives(s2, mass, area);

                State s3 = new State
                {
                    X = s.X + k2.X * dt * 0.5,
                    Y = s.Y + k2.Y * dt * 0.5,
                    Vx = s.Vx + k2.Vx * dt * 0.5,
                    Vy = s.Vy + k2.Vy * dt * 0.5
                };
                State k3 = GetDerivatives(s3, mass, area);

                State s4 = new State
                {
                    X = s.X + k3.X * dt,
                    Y = s.Y + k3.Y * dt,
                    Vx = s.Vx + k3.Vx * dt,
                    Vy = s.Vy + k3.Vy * dt
                };
                State k4 = GetDerivatives(s4, mass, area);

                s.X += (k1.X + 2 * k2.X + 2 * k3.X + k4.X) * dt / 6.0;
                s.Y += (k1.Y + 2 * k2.Y + 2 * k3.Y + k4.Y) * dt / 6.0;
                s.Vx += (k1.Vx + 2 * k2.Vx + 2 * k3.Vx + k4.Vx) * dt / 6.0;
                s.Vy += (k1.Vy + 2 * k2.Vy + 2 * k3.Vy + k4.Vy) * dt / 6.0;

                if (s.Y > maxY) maxY = s.Y;
                points.Add(new PointF((float)s.X, (float)s.Y));
            }

            return new SimulationResult
            {
                Range = s.X,
                MaxHeight = maxY,
                FinalSpeed = Math.Sqrt(s.Vx * s.Vx + s.Vy * s.Vy),
                Points = points
            };
        }

        private void btnLaunch_Click(object sender, EventArgs e)
        {
            animationTimer?.Stop();

            double dt = (double)numStep.Value;
            var result = Simulate(dt);
            trajectoryCounter++;

            activeSeries = new Series($"Траектория {trajectoryCounter}");
            activeSeries.ChartType = SeriesChartType.Spline;
            activeSeries.Color = Color.FromArgb(random.Next(50, 255), random.Next(50, 255), random.Next(50, 255));
            activeSeries.BorderWidth = 2;
            chartTrajectory.Series.Add(activeSeries);

            animationPoints = result.Points;
            currentPointIndex = 0;
            animationTimer.Start();

            dataGridViewResults.Rows.Add(
                dt.ToString("F4"),
                result.Range.ToString("F2"),
                result.MaxHeight.ToString("F2"),
                result.FinalSpeed.ToString("F2")
            );
        }

        private void AnimationTimer_Tick(object sender, EventArgs e)
        {
            if (currentPointIndex < animationPoints?.Count)
            {
                activeSeries.Points.AddXY(animationPoints[currentPointIndex].X, animationPoints[currentPointIndex].Y);
                currentPointIndex++;
            }
            else
            {
                animationTimer.Stop();
            }
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            animationTimer?.Stop();
            chartTrajectory.Series.Clear();
            dataGridViewResults.Rows.Clear();
            trajectoryCounter = 0;
        }
    }
}
```

## 3. Скриншот программы с несколькими траекториями

<img width="616" height="797" alt="image" src="https://github.com/user-attachments/assets/10fdfabc-38bc-4fd7-bf37-bd42919bef53" />

*Рисунок 1 — Интерфейс программы с результатами моделирования для различных шагов*

На графике отображены 5 траекторий, полученных при шагах моделирования: 1 с, 0.1 с, 0.01 с, 0.001 с, 0.0001 с. Каждая траектория имеет уникальный цвет и отображается в легенде.

## 4. Таблица результатов моделирования

| Шаг моделирования, с | 1 с | 0,1 с | 0,01 с | 0,001 с | 0,0001 с |
|:---------|:---------|:---------|:---------|:---------|:---------|
| **Дальность полёта, м** | 190,15 | 181,66 | 179,71 | 179,68 | 179,67 |
| **Максимальная высота, м** | 52,05 | 52,13 | 52,13 | 52,13 | 52,13 |
| **Скорость в конечной точке, м/с** | 39,02 | 37,07 | 36,64 | 36,63 | 36,63 |

**Параметры запуска:**
- Начальная высота: 0 м
- Начальная скорость: 50 м/с
- Угол запуска: 45°
- Масса тела: 1 кг
- Диаметр тела: 0,1 м

## 5. Выводы

В ходе выполнения лабораторной работы было разработано приложение для моделирования полёта тела в атмосфере с учётом силы тяжести и аэродинамического сопротивления, реализованное на C# с использованием Windows Forms. Проведение нескольких тестов с изменением шага моделирования показало, что при его уменьшении с 1 с до 0,1 с погрешность расчёта дальности значительно снижается, а при уменьшении с 0,01 с до 0,0001 с результаты имеют минимальную разницу, при этом значение максимальной высоты остаётся стабильным даже при крупных шагах. Программная реализация с сохранением прошлых траекторий и результатов предыдущих вычислений наглядно демонстрирует разницу значений при варьировании шага моделировании.

