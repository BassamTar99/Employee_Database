import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EmployeeDatabase:
    def __init__(self):
       self.employees={}


    def add_employee(self, emp_id, name="Unknown", department="N/A", salary=0, active=False):
        self.employees[emp_id] = {
            "name": name,
            "department": department,
            "salary": salary,
            "active": active,
        }
    def display_employees(self):
        for emp_id, details in self.employees.items():
            print(f"ID: {emp_id}, Details: {details}")

    def display_employees_names(self):
        emp_names=[details['name'] for details in self.employees.values()]
        print (f"Employees: {'-'.join(emp_names)}")


    def get_active_employees(self):
        return [details for details in self.employees.values() if details['active']]
    def get_employees_by_department(self, department):
        return {emp_id: details for emp_id, details in self.employees.items() if details['department'] == department}
    def mark_inactive(self, emp_ids):
        for emp_id in emp_ids:
            if emp_id in self.employees:
                self.employees[emp_id]['active'] = False
    def update_salary(self, emp_id, new_salary):
        if emp_id in self.employees:
            self.employees[emp_id]['salary'] = new_salary

    def ConvToDataframe(self):
        df= pd.DataFrame.from_dict(self.employees,orient='index')
        df['Annual_Bonus']=df['salary']*0.1
        df['Employment_Duration']=0

        return df
    def avg_salary_bydep(self):
        df=self.ConvToDataframe()
        return df.groupby('department')['salary'].mean()

    def highest_salary_dep(self):
        df=self.ConvToDataframe()
        dep_salary= df.groupby('department')['salary'].sum()
        return dep_salary.idxmax()

    def count_status(self):
        df=self.ConvToDataframe()
        act_count=df['active'].sum()
        inact_count= len(df)-act_count
        return act_count,inact_count
    def filter_employees(self, salary_threshold=0, department=None):
        df = self.ConvToDataframe()
        
        if salary_threshold !=0:
            df = df[df['salary'] > salary_threshold]
        
        if department != None :
            df = df[df['department'] == department]
        
        return df

    def export_to_csv(self, filename, salary_threshold=0, department=None):
        df = self.filter_employees(salary_threshold, department)
        df.to_csv(filename)

    def visualize_data(self):
        df=self.ConvToDataframe()
        department_count = df['department'].value_counts()
        department_count.plot(kind='bar', title='Number of Employees per Department', xlabel='Department', ylabel='Number of Employees')
        plt.show()

        
        active_inactive_count = df['active'].value_counts()
        active_inactive_count.plot(kind='pie', labels=['Active', 'Inactive'], autopct='%1.1f%%', title='Active vs Inactive Employees')
        plt.show()

    def load_data(self, file_path, dtype=None, encoding="utf-8"):
            self.employees = pd.read_csv(file_path, dtype=dtype, encoding=encoding).set_index('emp_id').to_dict(orient='index')
    def explore_data(self):
        df = self.ConvToDataframe()
        print(f"Dataset Dimensions: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("Column Types:")
        print(df.dtypes)

    def handle_missing_values(self):
        df = self.ConvToDataframe()
        print("Missing Values Per Column:")
        print(df.isnull().sum())
        df.fillna({"department": "Unknown", "salary": 0, "active": False}, inplace=True)
        print("Missing values handled.")

    def remove_duplicates(self):
        df = self.ConvToDataframe()
        before_count = len(df)
        df.drop_duplicates(inplace=True)
        after_count = len(df)
        print(f"Removed {before_count - after_count} duplicate rows.")



    def convert_data_types(self):
        df = self.ConvToDataframe()
        df["active"] = df["active"].astype(bool)
        df["salary"] = df["salary"].astype(float)
        print("Data types converted.")

    def add_features(self):
        df = self.ConvToDataframe() 
        print("Features added.")

    def summarize_data(self):
        df = self.ConvToDataframe()
        print("Summary Statistics:")
        print(df.describe())
        print("\nCorrelation Matrix:")
        print(df.corr())

    def visualize_data(self):
        df = self.ConvToDataframe()
        
        plt.figure(figsize=(8, 6))
        plt.hist(df['salary'], bins=5, color='skyblue', edgecolor='black')
        plt.title("Salary Distribution")
        plt.xlabel("Salary")
        plt.ylabel("Frequency")
        plt.show()
        







db = EmployeeDatabase()


db.add_employee("101", name="Hisham", department="HR", salary=50000, active=True)
db.add_employee("102", name="Dana", department="ML", salary=75000, active=True)
db.add_employee("103", name="Bassam", department="Intern",salary=30000, active=False)  
db.add_employee("104",name="Sarah", department="HR", salary=55000, active=True) 
db.add_employee("105", name="Dupl", department="HR", salary=55000, active=True)





df=db.ConvToDataframe()
print("\nDataFrame:")
print(df)

print("\nLoading data from CSV...")
db.load_data('employee_data.csv')
df = db.ConvToDataframe()
print("\nDataFrame after loading from CSV:")
print(df)

print("\nExploring data:")
db.explore_data()

print("\nHandling missing values:")
db.handle_missing_values()
df = db.ConvToDataframe()
print("\n After handling missing values:")
print(df)

print("\nRemoving duplicates:")
db.remove_duplicates()
df = db.ConvToDataframe()
print("\nDataFrame after removing duplicates:")
print(df)

print("\nConverting data types:")
db.convert_data_types()
df = db.ConvToDataframe()
print("\nDataFrame after converting data types:")
print(df.dtypes)

db.export_to_csv('filtered_employees.csv', salary_threshold=40000)

