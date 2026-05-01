import streamlit as st
import pandas as pd
from utils.data_loader import get_cleaned_data, get_cleaned_reviews, get_uncleaned_data

st.set_page_config(page_title="Rental Search", page_icon=":material/search:", layout="wide")

st.title("Rental Search & Details")
st.markdown("Search for a specific property by its title to see its full details.")

try:
    df = get_cleaned_data()
    titles = df['title'].dropna().unique().tolist()
    
    selected_title = st.selectbox(
        "Search by Listing Title", 
        options=titles, 
        index=None, 
        placeholder="Start typing a listing name..."
    )
    
    if selected_title:
        property_data = df[df['title'] == selected_title].iloc[0]
        
        df_uncleaned = get_uncleaned_data()
        uncleaned_match = df_uncleaned[df_uncleaned['title'] == selected_title].iloc[0]
        
        target_room_id = uncleaned_match.get('room_id', uncleaned_match.get('id'))
        property_url = uncleaned_match.get('url', uncleaned_match.get('listing_url'))
        
        st.divider()
        
        if pd.notna(property_url):
            st.markdown(f"## [{property_data['title']}]({property_url})")
        else:
            st.subheader(property_data['title'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (Total)", f"EGP {property_data['price_breakdown_baseprice_price']:,.2f}")
        col2.metric("Overall Rating", f"{property_data['rating_overall']} :material/star:")
        col3.metric("Reviews Count", int(property_data['reviews_count']))
        
        st.markdown("### Property Features")
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Bedrooms:** {property_data['bedrooms']}")
        c2.write(f"**Bathrooms:** {property_data['bathrooms']}")
        c3.write(f"**Description:** {property_data['description_length']} characters")
        
        st.markdown("### Amenities")
        c1, c2, c3 = st.columns(3)
        c1.write(f"**WiFi:** {'Yes' if property_data['has_wifi'] else 'No'}")
        c2.write(f"**Pool:** {'Yes' if property_data['has_pool'] else 'No'}")

        st.divider()

        st.subheader("Guest Feedback")
        
        try:
            df_reviews = get_cleaned_reviews()
            
            if target_room_id is not None and 'room_id' in df_reviews.columns:
                
                property_reviews = df_reviews[df_reviews['room_id'] == target_room_id]
                
                if not property_reviews.empty:
                    top_positive = property_reviews.sort_values(by='sentiment_score', ascending=False).head(3)
                    top_negative = property_reviews.sort_values(by='sentiment_score', ascending=True).head(3)
                    
                    rev_col1, rev_col2 = st.columns(2)
                    
                    with rev_col1:
                        st.markdown("#### :material/thumb_up: Best Reviews")
                        for _, row in top_positive.iterrows():
                            st.success(f"\"{row['comments']}\" \n\n*(Score: {row['sentiment_score']:.2f})*")
                            
                    with rev_col2:
                        st.markdown("#### :material/thumb_down: Worst Reviews")
                        for _, row in top_negative.iterrows():
                            st.error(f"\"{row['comments']}\" \n\n*(Score: {row['sentiment_score']:.2f})*")
                else:
                    st.info("No reviews have been scraped for this specific property.")
            else:
                st.warning("Cannot load reviews: Unable to find the room ID or the 'room_id' column is missing from the reviews dataset.")
                
        except FileNotFoundError:
            st.error("Could not find the reviews dataset. Please check your data_loader paths.")
            
        with st.expander("View Raw Data for this Listing"):
            st.dataframe(pd.DataFrame(property_data).T, use_container_width=True)
            
except FileNotFoundError:
    st.error("Could not find the dataset.")