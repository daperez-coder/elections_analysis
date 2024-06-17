import pandas as pd
import numpy as np
from sklearn.decomposition import SparsePCA, PCA, FastICA
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
import matplotlib.cm as cm
from matplotlib.lines import Line2D



# create a custom colormap with n_colors colors
colors = mplcolors.ListedColormap(cm.tab20.colors[:])


# Define a function to convert percentage strings to float
def convert_percentage_string(s):
    if isinstance(s, str):
        s = s.replace('%', '').replace(',', '.').strip()
        return float(s) / 100
    return s

def get_PCA(df_results, mask_calculate=None, method='sparse', alpha=0.5, n_components=3):
    if mask_calculate is not None:
        df = df_results[mask_calculate]
    else:
        df = df_results

    # Define the numerical columns
    numerical_columns = ['% Abstentions',  
                     '% Blancs/inscrits', '% Nuls/inscrits']

    # Dynamically add repeating columns for Voix, % Voix/inscrits, % Voix/exprimés
    num_panels = 38  # Assume there are 10 panels, adjust accordingly
    for i in range(1, num_panels + 1):
        numerical_columns.extend([f'% Voix/inscrits_{i}'])#, f'% Voix/exprimés_{i}', f'% Voix/inscrits_{i}', f'Voix_{i}'])
    print(numerical_columns)
    # Apply the conversion function to percentage columns
    for col in numerical_columns:
        if col in df.columns:
            df[col] = df[col].apply(convert_percentage_string)
    
    # Ensure the numerical columns exist in the DataFrame
    numerical_columns = [col for col in numerical_columns if col in df.columns]
    
    # Extract the numerical data
    numerical_data = df[numerical_columns] #- np.array(np.ones(len(numerical_columns))/len(numerical_columns))

    # Compute the PCA
    if method == 'sparse':
        pca = SparsePCA(n_components=n_components, alpha=alpha)
    elif method == 'ICA':
        pca = FastICA(n_components=n_components, max_iter=300)
    else:
        pca = PCA(n_components=n_components)

    pca_results = pca.fit_transform(numerical_data)
    return pca, pca_results


def plot_pca(pca, variable_names, pca_results, global_results, size=None, labels=None, mask=None, submask=None, method='PCA'):
    if mask is not None:
        pca_results = pca_results[mask]
    n = pca_results.shape[1]
    m = len(variable_names)
    directions = pca.transform(np.identity(m))
    total_results_proj = pca.transform(global_results.reshape(1, -1))
    
    size = 4 if size is None else (150 * size / np.max(size))
    
    fig, axes = plt.subplots(n, n, figsize=(15 * n, 10 * n))

    # Create custom legend
    total_res_df = pd.DataFrame(index=variable_names, columns=['results'], data=global_results)
    total_res_df.sort_values(by='results',inplace=True, ascending=False)
    legend_elements = [Line2D([0], [0], color=colors(i), lw=4, label=total_res_df.index[i]) for i in range(len(variable_names))]
    total_res_df['colors'] = [colors(i) for i in range(len(total_res_df.index))]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                axes[i, j].hist(pca_results[:, i], bins=20, alpha=0.75)
                axes[i, j].set_title(f'{method} {i + 1}')
                axes[i, j].set_xlabel('Value')
                axes[i, j].set_ylabel('Frequency')
            elif i>j:

                # Add labels to points
                if labels is not None:
                    for k, label in enumerate(labels):
                        axes[j, i].text(pca_results[k, i], pca_results[k, j], label, fontsize=8,) #bbox=dict(facecolor='white', alpha=0.5))

                if submask is not None:
                    axes[j, i].scatter(pca_results[~submask].T[i], pca_results[~submask].T[j], s=size, alpha=0.8)
                    axes[j, i].scatter(pca_results[submask].T[i], pca_results[submask].T[j], s=size, alpha=0.8)
                else:
                    axes[j, i].scatter(pca_results[:, i], pca_results[:, j], s=size, alpha=0.8)
                
                axes[j, i].scatter(total_results_proj.T[i], total_results_proj.T[j], marker='x', c='red', label='France entière')
                axes[j, i].set_xlabel(f'{method} {i + 1}')
                axes[j, i].set_ylabel(f'{method} {j + 1}')

                #l =0
                
                for k in range(directions.shape[0]):
                    thres = np.quantile(np.linalg.norm(directions[:, [i,j]], axis=1),0.5)
                    normalization = np.quantile(np.linalg.norm(directions[:, [i,j]], axis=1),0.9) if method == 'ICA' else 5
                    head_width = 0.02 if method=='ICA' else 0.005 
                    linewidth = 1.5 if method=='ICA' else 0.8
                    if np.linalg.norm(directions[k, [i, j]]) > thres:
                        arrow_color = total_res_df.loc[variable_names[k], 'colors']
                        axes[j, i].arrow(0, 0, directions[k, i] /normalization, directions[k, j] / normalization, color=arrow_color, alpha=0.8, linewidth=linewidth, head_width=head_width)
                        #axes[i, j].text(directions[k, i] * 1.1 / 3, directions[k, j] * 1.1 / 3, variable_names[k], color=arrow_color, ha='center', va='center', alpha=0.7)
                        #l+=1
                axes[j,i].legend()
            else:
                pass
    
    fig.legend(handles=legend_elements, loc='lower center', ncol=8, fontsize='large')
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)  # Adjust bottom margin to make space for the legends
    return fig, axes 


def plot_components(pca, variable_names):
    components = pca.components_


    # Create a custom diverging colormap
    #cmap = mcolors.TwoSlopeNorm(vmin=np.min(components), vcenter=0, vmax=np.max(components))
    
    # Set the figure size to be larger to accommodate all labels
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the heatmap
    im = ax.imshow(components, cmap='viridis', aspect='auto',)#norm=cmap)

    # Add colorbar
    plt.colorbar(im, ax=ax, label='Component Value')

    # Set x and y labels
    plt.xlabel('Axes')
    plt.ylabel('PCA vectors')

    # Set title
    plt.title('PCA Components Heatmap')

    # Set xticks with variable names using the dictionary
    plt.xticks(ticks=np.arange(components.shape[1]), labels=[variable_names[i] for i in range(components.shape[1])], rotation=45, ha='right')

    # Set yticks with variance explained
    plt.yticks(ticks=np.arange(components.shape[0]), labels=[f'Feature {i}' for i in range(components.shape[0])])
    plt.grid(None)
    # Adjust layout to fit all labels
    plt.tight_layout()
    plt.show()
    return fig, ax 