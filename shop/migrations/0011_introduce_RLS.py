from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0010_alter_listing_creator'),
    ]

    operations = [
        migrations.RunSQL("""
            -- Enable RLS on the listings table
            ALTER TABLE shop_listing ENABLE ROW LEVEL SECURITY;
            ALTER TABLE shop_listing FORCE ROW LEVEL SECURITY;
            -- Create function to get current user
            CREATE OR REPLACE FUNCTION current_user_id()
            RETURNS VARCHAR AS $$
            BEGIN
                RETURN current_setting('shop.current_user_id', TRUE);
            END;
            $$ LANGUAGE plpgsql;

            -- Create RLS policy
            CREATE POLICY listing_access_policy ON shop_listing
            FOR ALL
            USING
                (CASE
                    WHEN (((status)::text = 'active'::text) OR ((status)::text = 'reserved'::text)) THEN true
                    WHEN ((creator_id)::text = current_user_id()::text) THEN true
	                ELSE EXISTS (SELECT 1
   			            FROM public.auth_user au
  			            WHERE (au.is_superuser = true) 
			            AND ((au.id::text = current_user_id()::text)))
                END)
            WITH CHECK
                (CASE
                    WHEN ((creator_id)::text = (current_user_id())::text) THEN true
                    ELSE EXISTS ( SELECT 1
   			            FROM public.auth_user au
  			            WHERE (au.is_superuser = true) 
			            AND ((au.id::text = current_user_id()::text))) 
                END);
        """,
        """
            DROP POLICY IF EXISTS listing_access_policy ON shop_listing;
            DROP FUNCTION IF EXISTS current_user_id();
            ALTER TABLE shop_listing DISABLE ROW LEVEL SECURITY;
        """)
    ]