import sys
import pickle
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QMessageBox, QDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


global_piezo_sensitivity = 0.0 # or any default value you prefer
global_spring_constant=0.0
global_coef=0.0

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Ajoutez un bouton pour la sensibilité du piezo
        self.btn_piezo_sensitivity = QPushButton("Modifier la sensibilité du piezo")
        layout.addWidget(self.btn_piezo_sensitivity)
        self.btn_piezo_sensitivity.clicked.connect(self.parent().update_piezo_sensitivity)

        # Ajoutez un bouton pour la constante d'elasticite
        self.btn_spring_constant = QPushButton("Modifier la constante d'élasticité")
        layout.addWidget(self.btn_spring_constant)
        self.btn_spring_constant.clicked.connect(self.parent().update_spring_constant)
        
        # Ajoutez un bouton pour la constante d'elasticite
        self.btn_coef = QPushButton("Modifier la coef")
        layout.addWidget(self.btn_coef)
        self.btn_coef.clicked.connect(self.parent().coef)


class MainWindow(QMainWindow):

    
    def __init__(self):
        super().__init__()
        
        # Set window size
       # self.resize(1000, 1000)
        
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create figure and canvas
        self.figure = plt.figure(figsize=(14, 10))  # Set figure size here
        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)
        
        
        main_layout.addWidget(self.canvas)
        
        # Create labels for piezo sensitivity and spring constant
        self.lbl_piezo_sensitivity = QtWidgets.QLabel()
        main_layout.addWidget(self.lbl_piezo_sensitivity)
        self.lbl_spring_constant = QtWidgets.QLabel()
        main_layout.addWidget(self.lbl_spring_constant)
        self.lbl_coef = QtWidgets.QLabel()
        main_layout.addWidget(self.lbl_coef)

         
        # Create buttons and add to layout
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        load_txt_button = QPushButton('young modulus with pow function fit')
        button_layout.addWidget(load_txt_button)
        load_csv_button = QPushButton('yound modulus with linear fit')
        button_layout.addWidget(load_csv_button)
       
        self.change_saphir_button = QPushButton('Change Saphir File')
        button_layout.addWidget(self.change_saphir_button)
        
            # Create settings button
        settings_button = QPushButton('Settings')
        button_layout.addWidget(settings_button)
   
      


        # Connect buttons to functions
        load_txt_button.clicked.connect(self.load_txt)
        load_csv_button.clicked.connect(self.load_csv)
        settings_button.clicked.connect(self.open_settings)
        self.change_saphir_button.clicked.connect(self.change_saphir_file)
        # Set main widget
        self.setCentralWidget(main_widget)
    
       # Set global piezo sensitivity
        global global_piezo_sensitivity
        global_piezo_sensitivity = 206.0  # m/V
        self.lbl_piezo_sensitivity.setText("Sensibilité du piezo: {} e-9m/V".format(global_piezo_sensitivity))
        
         # Set global piezo sensitivity
        global global_spring_constant
        global_spring_constant = 0.2  # N/m
        self.lbl_spring_constant.setText("Constante d'élasticité': {} N/m".format(global_spring_constant))
        
        
         # Set global piezo sensitivity
        global global_coef
        global_coef = 8  # N/m
        self.lbl_coef.setText("coef': {} GPa".format(global_coef))
        
       
        try:
            with open('config.pkl', 'rb') as f:
                self.saphir_file_path = pickle.load(f)
        except FileNotFoundError:
            self.saphir_file_path = None 
    def update_piezo_sensitivity(self):
        global global_piezo_sensitivity # declare global variable
        # Créer un dialogue pour rentrer la nouvelle valeur de la sensibilité du piezo
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, "change piezo sensitivity ", "Entrez la nouvelle valeur pour la sensibilité du piezo 10^-9(m/V):", value=global_piezo_sensitivity, decimals=4)
        if ok:
            # Mettre à jour la valeur de piezo_sensitivity
            global_piezo_sensitivity = new_value
            # Mettre à jour l'étiquette
            self.lbl_piezo_sensitivity.setText("piezo sensitivity: {} m/V".format(global_piezo_sensitivity))

    def update_spring_constant(self):
        global global_spring_constant # declare global variable
        # Créer un dialogue pour rentrer la nouvelle valeur de la spring constant
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, "change spring constant", "Entrez la nouvelle valeur pour la contante d'élasticité (N/m):", value=global_spring_constant, decimals=4)
        if ok:
            # Mettre à jour la valeur de piezo_sensitivity
            global_spring_constant = new_value
            # Mettre à jour l'étiquette
            self.lbl_spring_constant.setText("spring constant': {} N/m".format(global_spring_constant))
            
    def coef(self):
        global global_coef # declare global variable
        # Créer un dialogue pour rentrer la nouvelle valeur de la spring constant
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, "coef", "Entrez la nouvelle valeur pour la ccoef (GPa):", value=global_coef, decimals=4)
        if ok:
            # Mettre à jour la valeur de piezo_sensitivity
            global_coef = new_value
            # Mettre à jour l'étiquette
            self.lbl_coef.setText("coefficient': {} GPa".format(global_coef))



     
    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()   
        
    def save_saphir_file_path(self):
        with open('config.pkl', 'wb') as f:
            pickle.dump(self.saphir_file_path, f)   
    def change_saphir_file(self):
        saphir_file_path, _ = QFileDialog.getOpenFileName(self, 'Open Saphir CSV', '.', 'CSV Files (*.csv);;All Files (*)')
        if saphir_file_path:
            self.saphir_file_path = saphir_file_path
            self.save_saphir_file_path()
            

     
    def load_txt(self):
        # Open file dialog to select TXT file
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '.', 'TXT Files (*.txt);;All Files (*)'
        )
    
        # If the user cancels the file dialog, do nothing
        if not filename:
            return
     
    
        try:
            # Load data from CSV file and rename columns
            df = pd.read_csv(filename, delimiter=';', header=None, names=['Z_piezo_voltage', 'X_deflection_voltage'])
            # Load data from second CSV file and rename columns

            
            # Convert Z_piezo_voltage to displacement in µm
            piezo_sensitivity = global_piezo_sensitivity * 1e-9  # m/V
            piezo_sensitivity_micrometerspervolts = piezo_sensitivity * 1e6  # micrometers/V
            df['Displacement (µm)'] = df['Z_piezo_voltage'].astype(float) * piezo_sensitivity_micrometerspervolts  # micrometers
            # Convert Z_piezo_voltage to displacement in µm for the second file
          
            
            # Convert X_deflection_voltage to force in nN
            cantilever_spring_constant = global_spring_constant  # N/m
            df['Force (nN)'] = df['X_deflection_voltage'].astype(float) * cantilever_spring_constant * piezo_sensitivity * 1e9
            
            
            # Shift the plot upwards by adding the negative value of the first point's force to all force values
            first_force_value = df['Force (nN)'].iloc[0]
            df['Force (nN)'] += abs(first_force_value).astype(float)
                     
            # Find the displacement value where df starts to rise
            start_df = df[df['Force (nN)'] > 0.05]['Displacement (µm)'].values[0]
            
            print(start_df)
    
            # Filter out points with force values within +/- 0.05 nN of 0 nN
            df_filtered = df.loc[(df['Force (nN)'] > 0.05) | (df['Force (nN)'] < -0.05)]
            
            # Find index of maximum force value
            max_force_index = df_filtered['Force (nN)'].idxmax()
            
            # Separate data into two parts based on maximum force index
            second_part = df_filtered.loc[max_force_index+1:]
    
          
    
            # Fit linear regression to second part
            x2 = second_part['Displacement (µm)'].values.reshape(-1, 1)
            y2 = second_part['Force (nN)'].values.reshape(-1, 1)
            
            # Define the form of the function you want to fit
            def power_law(x, alpha):
                return alpha * np.abs(x - h_f)**1.5
            
            # Provide a guess for the initial value of alpha
            initial_guess = [0.01]
            
            # Set bounds for alpha
            bounds = ([0.001], [1.0])
            
            # Trouver l'index de la valeur la plus proche de zéro dans y2
            idx = np.abs(y2 - 0).argmin()

            # Utiliser cet index pour obtenir la valeur correspondante de x2
            h_f = x2[idx]

            # Imprimer la valeur de x2 où y2 est le plus proche de zéro
            print(h_f)

            # curve_fit will return the optimized parameters and the covariance
            popt, pcov = curve_fit(power_law, x2.flatten(), y2.flatten(), p0=initial_guess, bounds=bounds)
            
            # popt contains the optimized parameters
            alpha_opt = popt[0]
            
            # now we can use alpha_opt to plot the fit:
            x_values = np.linspace(min(x2), max(x2), num=1000)
            y_values = power_law(x_values, alpha_opt)
            
            # Clear figure and plot data
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Plot all points in yellow
            ax.plot(df['Displacement (µm)'], df['Force (nN)'], '.', markersize=1, color='k')
          
            ax.plot(x_values, y_values, color='green')
            
            # Set axis labels and title
            ax.set_xlabel('Displacement (µm)')
            ax.set_ylabel('Force (nN)')
            # Set the plot title to the filename
            filename_title = "force distance curve of the sample : " + os.path.basename(filename)
            ax.set_title(filename_title)
              
    
            # Refresh canvas to display plot
            self.canvas.draw()
    
        except Exception as e:
            # Show an error message if the file can't be loaded or processed
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle('Error')
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText(f'Error loading TXT file: {e}')
            error_dialog.exec_()


            
 
    def load_csv(self):
        # Open file dialog to select CSV file
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', 'CSV Files (*.csv);;All Files (*)')
    
        # If the user cancels the file dialog, do nothing
        if not filename:
            return
    
        # Open file dialog to select Saphir CSV file
        if self.saphir_file_path is None:
            self.saphir_file_path, _ = QFileDialog.getOpenFileName(self, 'Open Saphir CSV', '.', 'CSV Files (*.csv);;All Files (*)')
    
        # If the user cancels the file dialog, do nothing
        if not self.saphir_file_path:
            return
        try:
            
            # Load data from CSV file and rename columns
            df = pd.read_csv(filename, delimiter=';', header=None, names=['Z_piezo_voltage', 'X_deflection_voltage'])
            # Load data from Saphir CSV file and rename columns
            df2 = pd.read_csv(self.saphir_file_path, delimiter=';', header=None, names=['Z_piezo_voltage', 'X_deflection_voltage'])


            
            # Convert Z_piezo_voltage to displacement in µm
            piezo_sensitivity = global_piezo_sensitivity * 1e-9  # m/V
            piezo_sensitivity_micrometerspervolts = piezo_sensitivity * 1e6  # micrometers/V
            df['Displacement (µm)'] = df['Z_piezo_voltage'].astype(float) * piezo_sensitivity_micrometerspervolts  # micrometers
            # Convert Z_piezo_voltage to displacement in µm for the second file
            df2['Displacement (µm)'] = df2['Z_piezo_voltage'].astype(float) * piezo_sensitivity_micrometerspervolts  # micrometers

           
            
            # Convert X_deflection_voltage to force in nN
            cantilever_spring_constant = global_spring_constant  # N/m
            df['Force (nN)'] = df['X_deflection_voltage'].astype(float) * cantilever_spring_constant * piezo_sensitivity * 1e9
            
             # Convert X_deflection_voltage to force in nN for the second file
            df2['Force (nN)'] = df2['X_deflection_voltage'].astype(float) * cantilever_spring_constant * piezo_sensitivity * 1e9
    
            # Shift the plot upwards by adding the negative value of the first point's force to all force values
            first_force_value = df['Force (nN)'].iloc[0]
            df['Force (nN)'] += abs(first_force_value).astype(float)
            
            # Shift the plot upwards by adding the negative value of the first point's force to all force values
            first_force_value = df2['Force (nN)'].iloc[0]
            df2['Force (nN)'] += abs(first_force_value).astype(float)
            
                   # Find the displacement value where df starts to rise
            start_df = df[df['Force (nN)'] > 0.05]['Displacement (µm)'].values[0]
            
            # Find the displacement value where df2 starts to rise
            start_df2 = df2[df2['Force (nN)'] > 0.05]['Displacement (µm)'].values[0]
            
            # Calculate the necessary shift in micrometers
            shift = start_df - start_df2
            
            # Shift the entire df2 curve
            df2['Displacement (µm)'] = df2['Displacement (µm)'] + shift

    
            # Filter out points with force values within +/- 0.05 nN of 0 nN
            df_filtered = df.loc[(df['Force (nN)'] > 0.05) | (df['Force (nN)'] < -0.05)]
            
            # Find index of maximum force value
            max_force_index = df_filtered['Force (nN)'].idxmax()
            
            # Separate data into two parts based on maximum force index
            first_part = df_filtered.loc[:max_force_index]
            second_part = df_filtered.loc[max_force_index+1:]
    
            # Fit linear regression to first part
            x1 = first_part['Displacement (µm)'].values.reshape(-1, 1)
            y1 = first_part['Force (nN)'].values.reshape(-1, 1)
            reg1 = LinearRegression().fit(x1, y1)
            slope1 = reg1.coef_[0][0]
            r_sq1 = reg1.score(x1, y1)
    
            # Fit linear regression to second part
            x2 = second_part['Displacement (µm)'].values.reshape(-1, 1)
            y2 = second_part['Force (nN)'].values.reshape(-1, 1)
            reg2 = LinearRegression().fit(x2, y2)
            slope2 = reg2.coef_[0][0]
            r_sq2 = reg2.score(x2, y2)
            
            # Filter out points with force values within +/- 0.05 nN of 0 nN
            df_filtered2 = df2.loc[(df2['Force (nN)'] > 0.05) | (df2['Force (nN)'] < -0.05)]
            
            # Find index of maximum force value
            max_force_index = df_filtered2['Force (nN)'].idxmax()
            
            # Separate data into two parts based on maximum force index
            first_part2 = df_filtered2.loc[:max_force_index]
            second_part2 = df_filtered2.loc[max_force_index+1:]
    
    
            # Fit linear regression to first part
            x3 = first_part2['Displacement (µm)'].values.reshape(-1, 1)
            y3 = first_part2['Force (nN)'].values.reshape(-1, 1)
            reg3 = LinearRegression().fit(x3, y3)
            slope3 = reg3.coef_[0][0]
            r_sq3 = reg3.score(x3, y3)
    
            # Fit linear regression to second part
            x4 = second_part2['Displacement (µm)'].values.reshape(-1, 1)
            y4 = second_part2['Force (nN)'].values.reshape(-1, 1)
            reg4 = LinearRegression().fit(x4, y4)
            slope4 = reg4.coef_[0][0]
            r_sq4 = reg4.score(x4, y4)
            
            # Define the functions f(x) and g(x) using the regression objects
            def f(x):
                return reg1.coef_[0][0] * x + reg1.intercept_[0]

            def g(x):
                return reg3.coef_[0][0] * x + reg3.intercept_[0]

            # Define the range of x
            x_range = np.concatenate((x3.flatten(), x4.flatten()))
            
            # Find the value of x that gives the maximum value of g(x)
            x_last = max(x_range, key=g)
            
            # Calculate the value of g(x) at x_last
            g_val = g(x_last)
            
            # Find the value of x for which g(x) is equal to f_val
            x_g = (g_val - reg1.intercept_[0]) / reg1.coef_[0][0]
            
            # Calculate the horizontal distance
            young_first_part = abs(x_last - x_g)
            
            print(f"The yound modulus first part is {young_first_part}")
            
             # Define the functions f(x) and g(x) using the regression objects
            def f2(x):
                return reg2.coef_[0][0] * x + reg2.intercept_[0]

            def g2(x):
                return reg4.coef_[0][0] * x + reg4.intercept_[0]

            # Define the range of x
            x_range = np.concatenate((x3.flatten(), x4.flatten()))
            
            # Find the value of x that gives the maximum value of f(x)
            x_last2 = max(x_range, key=g2)
            
            # Calculate the value of f(x) at x_last
            g_val2 = g2(x_last)
            
            # Find the value of x for which g(x) is equal to f_val
            x_g2 = (g_val2 - reg2.intercept_[0]) / reg2.coef_[0][0]
            
            # Calculate the horizontal distance
            young_second_part = abs(x_last2 - x_g2)
            
            print(f"The yound modulus first part is {young_second_part}")
            
            # Calculate the minimum value of the y-axis in the second part data
            y2_min = y2.min()
            c=global_coef*1e9
            modulus=c*young_first_part
            print(f"The yound modulus is {modulus}")
                       
    
            # Clear figure and plot data
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
             
         
            
            # Plot all points in yellow
            ax.plot(df['Displacement (µm)'], df['Force (nN)'], '.', markersize=2, color='k')
            
            # Plot points from the second file in green
            ax.plot(df2['Displacement (µm)'], df2['Force (nN)'], '.', markersize=2, color='green')
            
            # Plot linear regression line with red color
       
            line1, = ax.plot(x1, reg1.predict(x1),'--', color='red')
    
            # Plot linear regression line with blue color
      
            line2, = ax.plot(x2, reg2.predict(x2),'--', color='blue')
            
             # Plot linear regression line with red color
       
            line3, = ax.plot(x3, reg3.predict(x3),'-', color='green')
    
            # Plot linear regression line with blue color
      
            line4, = ax.plot(x4, reg4.predict(x4),'-', color='green')
            
            # Plot horizontal line for Young's modulus
            line5 = ax.hlines(g_val, x_last, x_g, colors='purple', linestyles='dashed')
            
            # Plot horizontal line for Young's modulus
            line6 = ax.hlines(g_val2, x_last2, x_g2, colors='purple', linestyles='dashed')
            
            # Add a point for y2_min
            line7, = ax.plot(x2[y2.argmin()], y2_min, 'yo', markersize=5)

            # Set axis labels and title
            ax.set_xlabel('Displacement (µm)')
            ax.set_ylabel('Force (nN)')
            # Set the plot title to the filename
            filename_title = "force distance curve of the sample : " + os.path.basename(filename)
            ax.set_title(filename_title)
            
            
                   # Create the custom legend entries for Young's modulus
            legend_entry1 = f'h_c - First part: {young_first_part:.2f} µm'
            legend_entry2 = f'h_c - Second part: {young_second_part:.2f} µm'
            legend_entry3 = f'adhesion force: {y2_min:.2f} nN'
           
            # Add modulus value to the plot
            modulus_text = f'Young modulus: {modulus:.2f} GPa'
            ax.text(0.65, 0.05, modulus_text, transform=ax.transAxes, fontsize=10,
                    verticalalignment='top')
            
            # Add legend
            ax.legend([line1, line2, line3, line4,line5,line6,line7], [
                f'First part (R²={r_sq1:.2f}, slope={slope1:.2f} nN/µm)', 
                f'Second part (R²={r_sq2:.2f}, slope={slope2:.2f} nN/µm)',
                f'First part SAPHIR (R²={r_sq3:.2f}, slope={slope3:.2f} nN/µm)',
                f'Second part SAPHIR (R²={r_sq4:.2f}, slope={slope4:.2f} nN/µm)',
                legend_entry1,
                legend_entry2,
                legend_entry3

            ])
           
     
         
            # Refresh canvas to display plot
            self.canvas.draw()


    
        except Exception as e:
            # Show an error message if the file can't be loaded or processed
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle('Error')
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText(f'Error loading CSV file: {e}')
            error_dialog.exec_()




if __name__ == '__main__':
    # Create application
    app = QApplication(sys.argv)

    # Create main window
    main_window = MainWindow()
    main_window.show()

    # Run application
    sys.exit(app.exec_())