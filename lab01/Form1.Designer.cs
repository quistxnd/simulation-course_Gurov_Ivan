namespace lab1
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            panelParams = new Panel();
            lblParamsTitle = new Label();
            lblInitHeight = new Label();
            numInitHeight = new NumericUpDown();
            lblVelocity = new Label();
            numVelocity = new NumericUpDown();
            lblAngle = new Label();
            numAngle = new NumericUpDown();
            lblMass = new Label();
            numMass = new NumericUpDown();
            lblStep = new Label();
            numStep = new NumericUpDown();
            lblDiameter = new Label();
            numDiameter = new NumericUpDown();
            btnLaunch = new Button();
            btnClear = new Button();
            chartTrajectory = new System.Windows.Forms.DataVisualization.Charting.Chart();
            dataGridViewResults = new DataGridView();
            panelParams.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)numInitHeight).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numVelocity).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numAngle).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numMass).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numStep).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numDiameter).BeginInit();
            ((System.ComponentModel.ISupportInitialize)chartTrajectory).BeginInit();
            ((System.ComponentModel.ISupportInitialize)dataGridViewResults).BeginInit();
            SuspendLayout();

            // panelParams

            panelParams.BackColor = Color.FromArgb(240, 240, 240);
            panelParams.Controls.Add(lblParamsTitle);
            panelParams.Controls.Add(lblInitHeight);
            panelParams.Controls.Add(numInitHeight);
            panelParams.Controls.Add(lblVelocity);
            panelParams.Controls.Add(numVelocity);
            panelParams.Controls.Add(lblAngle);
            panelParams.Controls.Add(numAngle);
            panelParams.Controls.Add(lblMass);
            panelParams.Controls.Add(numMass);
            panelParams.Controls.Add(lblStep);
            panelParams.Controls.Add(numStep);
            panelParams.Controls.Add(lblDiameter);
            panelParams.Controls.Add(numDiameter);
            panelParams.Controls.Add(btnLaunch);
            panelParams.Controls.Add(btnClear);
            panelParams.Dock = DockStyle.Top;
            panelParams.Location = new Point(0, 0);
            panelParams.Name = "panelParams";
            panelParams.Size = new Size(616, 119);
            panelParams.TabIndex = 0;

            // lblParamsTitle

            lblParamsTitle.AutoSize = true;
            lblParamsTitle.Location = new Point(12, 12);
            lblParamsTitle.Name = "lblParamsTitle";
            lblParamsTitle.Size = new Size(116, 15);
            lblParamsTitle.TabIndex = 0;
            lblParamsTitle.Text = "Параметры запуска";

            // lblInitHeight

            lblInitHeight.AutoSize = true;
            lblInitHeight.Location = new Point(233, 12);
            lblInitHeight.Name = "lblInitHeight";
            lblInitHeight.Size = new Size(97, 15);
            lblInitHeight.TabIndex = 1;
            lblInitHeight.Text = "Нач. высота (м):";

            // numInitHeight

            numInitHeight.DecimalPlaces = 2;
            numInitHeight.Location = new Point(236, 30);
            numInitHeight.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            numInitHeight.Name = "numInitHeight";
            numInitHeight.Size = new Size(80, 23);
            numInitHeight.TabIndex = 2;
 
            // lblVelocity

            lblVelocity.AutoSize = true;
            lblVelocity.Location = new Point(375, 12);
            lblVelocity.Name = "lblVelocity";
            lblVelocity.Size = new Size(93, 15);
            lblVelocity.TabIndex = 3;
            lblVelocity.Text = "Скорость (м/с):";

            // numVelocity

            numVelocity.DecimalPlaces = 2;
            numVelocity.Location = new Point(378, 30);
            numVelocity.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            numVelocity.Name = "numVelocity";
            numVelocity.Size = new Size(80, 23);
            numVelocity.TabIndex = 4;
            numVelocity.Value = new decimal(new int[] { 50, 0, 0, 0 });

            // lblAngle

            lblAngle.AutoSize = true;
            lblAngle.Location = new Point(521, 12);
            lblAngle.Name = "lblAngle";
            lblAngle.Size = new Size(71, 15);
            lblAngle.TabIndex = 5;
            lblAngle.Text = "Угол (град):";

            // numAngle

            numAngle.DecimalPlaces = 2;
            numAngle.Location = new Point(524, 30);
            numAngle.Maximum = new decimal(new int[] { 90, 0, 0, 0 });
            numAngle.Name = "numAngle";
            numAngle.Size = new Size(80, 23);
            numAngle.TabIndex = 6;
            numAngle.Value = new decimal(new int[] { 45, 0, 0, 0 });

            // lblMass

            lblMass.AutoSize = true;
            lblMass.Location = new Point(233, 62);
            lblMass.Name = "lblMass";
            lblMass.Size = new Size(67, 15);
            lblMass.TabIndex = 7;
            lblMass.Text = "Масса (кг):";

            // numMass

            numMass.DecimalPlaces = 3;
            numMass.Location = new Point(236, 80);
            numMass.Maximum = new decimal(new int[] { 1000, 0, 0, 0 });
            numMass.Name = "numMass";
            numMass.Size = new Size(80, 23);
            numMass.TabIndex = 8;
            numMass.Value = new decimal(new int[] { 1, 0, 0, 0 });

            // lblStep

            lblStep.AutoSize = true;
            lblStep.Location = new Point(375, 62);
            lblStep.Name = "lblStep";
            lblStep.Size = new Size(140, 15);
            lblStep.TabIndex = 9;
            lblStep.Text = "Шаг моделирования (с):";

            // numStep

            numStep.DecimalPlaces = 4;
            numStep.Increment = new decimal(new int[] { 1, 0, 0, 262144 });
            numStep.Location = new Point(378, 80);
            numStep.Maximum = new decimal(new int[] { 1, 0, 0, 0 });
            numStep.Name = "numStep";
            numStep.Size = new Size(80, 23);
            numStep.TabIndex = 10;
            numStep.Value = new decimal(new int[] { 1, 0, 0, 65536 });

            // lblDiameter

            lblDiameter.AutoSize = true;
            lblDiameter.Location = new Point(521, 62);
            lblDiameter.Name = "lblDiameter";
            lblDiameter.Size = new Size(78, 15);
            lblDiameter.TabIndex = 11;
            lblDiameter.Text = "Диаметр (м):";

            // numDiameter

            numDiameter.DecimalPlaces = 3;
            numDiameter.Location = new Point(524, 80);
            numDiameter.Maximum = new decimal(new int[] { 10, 0, 0, 0 });
            numDiameter.Name = "numDiameter";
            numDiameter.Size = new Size(80, 23);
            numDiameter.TabIndex = 12;
            numDiameter.Value = new decimal(new int[] { 1, 0, 0, 65536 });

            // btnLaunch

            btnLaunch.Location = new Point(12, 30);
            btnLaunch.Name = "btnLaunch";
            btnLaunch.Size = new Size(110, 30);
            btnLaunch.TabIndex = 13;
            btnLaunch.Text = "Запустить";
            btnLaunch.UseVisualStyleBackColor = true;
            btnLaunch.Click += btnLaunch_Click;

            // btnClear

            btnClear.Location = new Point(12, 66);
            btnClear.Name = "btnClear";
            btnClear.Size = new Size(110, 30);
            btnClear.TabIndex = 14;
            btnClear.Text = "Очистить";
            btnClear.UseVisualStyleBackColor = true;
            btnClear.Click += btnClear_Click;

            // chartTrajectory

            chartArea1.Name = "ChartArea1";
            chartTrajectory.ChartAreas.Add(chartArea1);
            chartTrajectory.Location = new Point(12, 125);
            chartTrajectory.Name = "chartTrajectory";
            chartTrajectory.Size = new Size(592, 353);
            chartTrajectory.TabIndex = 1;
            chartTrajectory.Text = "chart1";

            // dataGridViewResults

            dataGridViewResults.AllowUserToAddRows = false;
            dataGridViewResults.AllowUserToDeleteRows = false;
            dataGridViewResults.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewResults.Location = new Point(12, 493);
            dataGridViewResults.Name = "dataGridViewResults";
            dataGridViewResults.Size = new Size(592, 294);
            dataGridViewResults.TabIndex = 2;

            // Form1

            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(616, 797);
            Controls.Add(dataGridViewResults);
            Controls.Add(chartTrajectory);
            Controls.Add(panelParams);
            Name = "Form1";
            Text = "Моделирование полёта тела";
            panelParams.ResumeLayout(false);
            panelParams.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)numInitHeight).EndInit();
            ((System.ComponentModel.ISupportInitialize)numVelocity).EndInit();
            ((System.ComponentModel.ISupportInitialize)numAngle).EndInit();
            ((System.ComponentModel.ISupportInitialize)numMass).EndInit();
            ((System.ComponentModel.ISupportInitialize)numStep).EndInit();
            ((System.ComponentModel.ISupportInitialize)numDiameter).EndInit();
            ((System.ComponentModel.ISupportInitialize)chartTrajectory).EndInit();
            ((System.ComponentModel.ISupportInitialize)dataGridViewResults).EndInit();
            ResumeLayout(false);
        }

        private System.Windows.Forms.Panel panelParams;
        private System.Windows.Forms.Label lblParamsTitle;
        private System.Windows.Forms.Label lblInitHeight;
        private System.Windows.Forms.NumericUpDown numInitHeight;
        private System.Windows.Forms.Label lblVelocity;
        private System.Windows.Forms.NumericUpDown numVelocity;
        private System.Windows.Forms.Label lblAngle;
        private System.Windows.Forms.NumericUpDown numAngle;
        private System.Windows.Forms.Label lblMass;
        private System.Windows.Forms.NumericUpDown numMass;
        private System.Windows.Forms.Label lblStep;
        private System.Windows.Forms.NumericUpDown numStep;
        private System.Windows.Forms.Label lblDiameter;
        private System.Windows.Forms.NumericUpDown numDiameter;
        private System.Windows.Forms.Button btnLaunch;
        private System.Windows.Forms.Button btnClear;
        private System.Windows.Forms.DataVisualization.Charting.Chart chartTrajectory;
        private System.Windows.Forms.DataGridView dataGridViewResults;
    }
}