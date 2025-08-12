#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import pandas as pd


# ## 1. Carga de Datos

# In[2]:


ventas_df = pd.read_csv('dataset_ventas.csv')
ventas_df.info()


# In[3]:


ventas_df.head()


# ## 2. Visualización Inicial

# In[4]:


print("Numero de unidades por venta y que productos son esas unidades")
sns.histplot(data=ventas_df, x='Unidades', bins=20, hue='Producto', multiple='stack'
             );


# ## 3. Gráficos Estadísticos Varidados

# ### Ventas Por Región del Año 2024
# **Graficos de Lineas Comparando totak de ventas por region en 2024**

# In[5]:


ventas_df['MesPeriodo'] = [pd.Period(fs, 'M') for fs in ventas_df.Fecha]
ventas_df


# In[6]:


ventas_por_periodo = ventas_df.groupby(by=['MesPeriodo', 'Región']).TotalVenta.sum().to_frame().reset_index()
ventas_por_periodo


# In[12]:


lim_sup = pd.Period('2025-01-01', 'M')
lim_inf = pd.Period('2024-01-01', 'M')
ventas_2024 = ventas_por_periodo[(ventas_por_periodo.MesPeriodo >= lim_inf) & (ventas_por_periodo.MesPeriodo < lim_sup)]
ventas_2024['MesPeriodo_'] = [f.to_timestamp() for f in ventas_2024['MesPeriodo']]


# In[8]:


sns.lineplot(data=ventas_2024, x='MesPeriodo_', y='TotalVenta', hue='Región')


# ### Gráfico de barras comparando categorías

# #### Ventas segun el tipo de Prodcuto y histograma de precios vendidos
# 

# In[40]:


# Filtrar para tener precios únicos por producto
precios_unicos = ventas_df.drop_duplicates(subset=["Producto", "PrecioUnitario"])

# Crear FacetGrid
g = sns.FacetGrid(precios_unicos, col="Producto", col_wrap=2, height=3)
g.map(sns.histplot, "PrecioUnitario", bins=10)
g.savefig('grafico-barras.pdf')




# In[ ]:





# #### Ventas Por Region Comparando el Total de Venta entre Productos

# In[13]:


ventas_por_region = ventas_df.groupby(by=['Región','Producto']).TotalVenta.sum().to_frame()


# In[11]:


sns.barplot(data=ventas_por_region, y='TotalVenta', x='Región', hue='Producto')


# ### Grafico de Dispersion comparando ventas en distintas regiones en 2024

# In[41]:


ventas_df['Mes_ord'] = pd.to_datetime(ventas_df.Fecha).dt.month 
ventas_por_numero_mes = ventas_df.groupby(by=['Mes_ord', 'Producto']).Unidades.sum().reset_index()


# In[36]:


scatter = sns.scatterplot(data=ventas_por_numero_mes, x='Mes_ord', y='Unidades', hue='Producto')
scatter.get_figure().savefig('grafico-dispersion.png')


# # Informe
# 
# No se observa ninguna tendencia en los datos de ventas. Además, todo indica que estos datos han sido generados artificialmente mediante métodos aleatorios.

# In[ ]:




