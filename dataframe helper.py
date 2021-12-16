import pandas as pd
import numpy as np

def df_info_func(df, vizualize=False, threshold=3, display_sample=True, sample_count = 5,side_by_side=True):
    def f1(series):
        try: return str(series.unique().tolist())
        except: return '--'

    print(f'Rows: {df.shape[0]} N Cols: {df.shape[1]}')

    if df.shape[0] > 0:
        df_info = pd.DataFrame(index=df.columns)
        df_info['data_types'] = df.dtypes.values
        df_info['n_missing'] = df.isna().sum().values    
        df_info['missing_pct'] = round((df_info['n_missing'] / len(df))*100,2)

        df_ = df.astype(str).copy()

        df_info['n_unique'] = df_.apply(lambda x: x.nunique(),axis=0).values
        df_info['uniq_vals'] = df_.apply(lambda x: np.where(x.nunique() <= threshold, f1(x), '--')).values

        for c in df.columns:            
            if df[c].dtype == 'datetime64[ns]':
                dt_str = "From: " + df[c].min().strftime('%d-%b-%Y')
                dt_str += " Till: " + df[c].max().strftime('%d-%b-%Y')
                df_info.loc[c,'uniq_vals'] = dt_str                
            elif df[c].dtype == 'float64' or  df[c].dtype == 'int64':
                real_num_series = df[c].dropna()
                if len(real_num_series) > 0:
                    dt_str = "Min: " + str(int(real_num_series.min()))
                    dt_str += " Max: " + str(int(real_num_series.max()))
                    dt_str += " Mean: " + str(int(real_num_series.mean()))
                    dt_str += " Med: " + str(int(real_num_series.median()))
                    dt_str += " Std: " + str(int(real_num_series.std()))
                else:
                    dt_str = ""
                df_info.loc[c,'uniq_vals'] = dt_str
            else:
                pass
                
        df_info.reset_index(inplace=True)
        df_info.rename(columns={'index':'cols'},inplace=True)
        if vizualize:
            # import seaborn as sns
            # sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
            # or an another package to display missing values graph
            import missingno as msno 
            msno.matrix(df)

        sample_df = pd.concat([df.head(sample_count),df.tail(sample_count)])
		
		if side_by_side:
            from IPython.display import display_html
            space = "\xa0" * 10
            info_styler = df_info.style.set_table_attributes("style='display:inline'").set_caption('DF Info')
            df_styler = sample_df.style.set_table_attributes("style='display:inline'").set_caption('DF')
            display_html(info_styler._repr_html_() + space + df_styler._repr_html_(),raw=True)            
        else:
            from IPython.core.display import HTML
            display(HTML(df_info.to_html()))
            if display_sample: 				
				display(HTML(sample_df.to_html()))            
    else:
        print("Empty DataFrame")