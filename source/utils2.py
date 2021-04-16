def pd_to_scipy_sparse_matrix(df):
    """
    Converts a sparse pandas data frame to sparse scipy csr_matrix.
    :param df: pandas data frame
    :return: csr_matrix
    """
    from scipy.sparse import lil_matrix
    arr = lil_matrix(df.shape, dtype=np.float32)
    for i, col in enumerate(df.columns):
        ix = df[col] != 0
        arr[np.where(ix), i] = 1

    return arr.tocsr()

        
def pd_plot_multi(data, cols=None, spacing=.1, **kwargs):

    from pandas import plotting
    from pandas.plotting import _matplotlib

    # Get default color style from pandas - can be changed to any other color list
    if cols is None: cols = data.columns
    if len(cols) == 0: return
    colors = getattr(getattr(plotting, '_matplotlib').style, '_get_standard_colors')(num_colors=len(cols))

    # First axis
    ax = data.loc[:, cols[0]].plot(label=cols[0], color=colors[0], **kwargs)
    ax.set_ylabel(ylabel=cols[0])
    lines, labels = ax.get_legend_handles_labels()

    for n in range(1, len(cols)):
        # Multiple y-axes
        ax_new = ax.twinx()
        ax_new.spines['right'].set_position(('axes', 1 + spacing * (n - 1)))
        data.loc[:, cols[n]].plot(ax=ax_new, label=cols[n], color=colors[n % len(colors)], **kwargs)
        ax_new.set_ylabel(ylabel=cols[n])

        # Proper legend position
        line, label = ax_new.get_legend_handles_labels()
        lines += line
        labels += label

    ax.legend(lines, labels, loc=0)
    return ax


def train_split_time(df, test_period = 40, cols=None , coltime ="time_key", sort=True, minsize=5,
                     n_sample=5,
                     verbose=False) :  
   cols = list(df.columns) if cols is None else cols    
   if sort :
       df   = df.sort_values( coltime, ascending=1 ) 
   #imax = len(df) - test_period   
   colkey = [ t for t in cols if t not in [coltime] ]  #### All time reference be removed
   if verbose : log(colkey)
   imax = test_period * n_sample ## Over sampling
   df1  = df.groupby( colkey ).apply(lambda dfi : dfi.iloc[:max(minsize, len(dfi) -imax), :] ).reset_index(colkey, drop=True).reset_index(drop=True)
   df2  = df.groupby( colkey ).apply(lambda dfi : dfi.iloc[max(minsize,  len(dfi) -imax):, :] ).reset_index(colkey, drop=True).reset_index(drop=True)  
   return df1, df2

        
def pd_to_keyvalue_dict(dfa, colkey= [ "shop_id", "l2_genre_id" ]   , col_list='item_id',  to_file=""):
    import copy, pickle
    dfa = copy.deepcopy(dfa)  
    def to_key(x):
        return "_".join([ str(x[t]) for t in colkey  ])
                
    dfa["__key"] = dfa.apply( lambda x :  to_key(x) , axis=1  )
    # dd = pd.DataFrame( dfa.groupby([ "__key"  ]).apply(lambda dfi :  [  int(t) for t in  dfi['item_id'].values] ) )  
    dd = pd.DataFrame( dfa.groupby([ "__key"  ]).apply(lambda dfi :    dfi[col_list].values ) )  
    dd.columns = ['__val']
    dd = dd.to_dict("dict")['__val']
    save(dd, to_file)


def pd_filter2(df, filter="16,*,*", col_plot=None, 
               lref = [ "shop_id", "dept_id", "l1_genre_id", "l2_genre_id","item_id" ]):    
    fl   = filter.split(",")
    for ii, x in enumerate(fl) :
        if x =="*" : continue
        df = df[df[ lref[ii] ] == int(x) ]    
        
    if col_plot: 
        df.set_index("time_key")[col_plot].plot()
    return df




def pd_cartesian(df1, df2) :
  col1 =  list(df1.columns)  
  col2 =  list(df2.columns)    
  df1['xxx'] = 1
  df2['xxx'] = 1    
  df3 = pd.merge(df1, df2,on='xxx')[ col1 + col2 ]
  return df3


def pd_histo(dfi, path_save=None, nbin=20.0, show=False) :  
  q0 = dfi.quantile(0.05)
  q1 = dfi.quantile(0.95)
  dfi.hist( bins=np.arange( q0, q1,  (  q1 - q0 ) /nbin  ) )
  os.makedirs(os.path.dirname(path_save), exist_ok=True)
  if path_save is not None : plt.savefig( path_save );   
  if show : plt.show(); 
  plt.close()

